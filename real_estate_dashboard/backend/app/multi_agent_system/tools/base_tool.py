"""
Base tool system for agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from loguru import logger


class BaseTool(ABC):
    """Base class for all tools."""

    def __init__(self, name: str, description: str = ""):
        """
        Initialize tool.

        Args:
            name: Tool name
            description: Tool description
        """
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """
        Execute the tool.

        Returns:
            Tool execution result
        """
        pass

    def to_dict(self) -> Dict[str, str]:
        """Convert tool to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
        }


class FileOperationsTool(BaseTool):
    """Tool for file operations."""

    def __init__(self):
        super().__init__(
            name="file_operations",
            description="Read, write, and manipulate files"
        )

    async def execute(
        self,
        operation: str,
        path: str,
        content: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute file operation.

        Args:
            operation: Operation type (read, write, append, delete)
            path: File path
            content: Content for write/append operations

        Returns:
            Operation result
        """
        try:
            if operation == "read":
                with open(path, "r") as f:
                    data = f.read()
                return {"success": True, "data": data}

            elif operation == "write":
                with open(path, "w") as f:
                    f.write(content or "")
                return {"success": True, "message": f"Written to {path}"}

            elif operation == "append":
                with open(path, "a") as f:
                    f.write(content or "")
                return {"success": True, "message": f"Appended to {path}"}

            elif operation == "delete":
                import os
                os.remove(path)
                return {"success": True, "message": f"Deleted {path}"}

            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}

        except Exception as e:
            logger.error(f"File operation error: {e}")
            return {"success": False, "error": str(e)}


class DataProcessingTool(BaseTool):
    """Tool for data processing operations."""

    def __init__(self):
        super().__init__(
            name="data_processing",
            description="Process and analyze data"
        )

    async def execute(
        self,
        operation: str,
        data: Any,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute data processing operation.

        Args:
            operation: Operation type (summarize, filter, transform, etc.)
            data: Data to process

        Returns:
            Processing result
        """
        try:
            if operation == "summarize":
                if isinstance(data, list):
                    return {
                        "success": True,
                        "summary": {
                            "count": len(data),
                            "type": "list",
                            "sample": data[:5] if len(data) > 5 else data,
                        }
                    }
                elif isinstance(data, dict):
                    return {
                        "success": True,
                        "summary": {
                            "keys": list(data.keys()),
                            "count": len(data),
                            "type": "dict",
                        }
                    }
                else:
                    return {
                        "success": True,
                        "summary": {
                            "type": type(data).__name__,
                            "value": str(data)[:100],
                        }
                    }

            elif operation == "filter":
                # Simple filtering example
                condition = kwargs.get("condition", lambda x: True)
                if isinstance(data, list):
                    filtered = [item for item in data if condition(item)]
                    return {"success": True, "data": filtered}
                else:
                    return {"success": False, "error": "Filter requires list data"}

            elif operation == "transform":
                # Simple transformation example
                transform_fn = kwargs.get("transform", lambda x: x)
                if isinstance(data, list):
                    transformed = [transform_fn(item) for item in data]
                    return {"success": True, "data": transformed}
                else:
                    return {"success": True, "data": transform_fn(data)}

            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}

        except Exception as e:
            logger.error(f"Data processing error: {e}")
            return {"success": False, "error": str(e)}


class CodeExecutionTool(BaseTool):
    """Tool for safe code execution."""

    def __init__(self, sandbox_mode: bool = True):
        super().__init__(
            name="code_execution",
            description="Execute code in a safe environment"
        )
        self.sandbox_mode = sandbox_mode

    async def execute(
        self,
        code: str,
        language: str = "python",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute code safely.

        Args:
            code: Code to execute
            language: Programming language
            **kwargs: Additional execution parameters

        Returns:
            Execution result
        """
        if language != "python":
            return {
                "success": False,
                "error": f"Unsupported language: {language}"
            }

        try:
            # In sandbox mode, we use restricted execution
            if self.sandbox_mode:
                # Create restricted globals/locals
                restricted_globals = {
                    "__builtins__": {
                        "print": print,
                        "len": len,
                        "range": range,
                        "str": str,
                        "int": int,
                        "float": float,
                        "list": list,
                        "dict": dict,
                        "sum": sum,
                        "max": max,
                        "min": min,
                    }
                }
                result_locals = {}

                # Execute code
                exec(code, restricted_globals, result_locals)

                return {
                    "success": True,
                    "result": result_locals.get("result", "Code executed successfully"),
                    "output": result_locals,
                }
            else:
                # WARNING: Unrestricted execution - use with caution
                exec_globals = {}
                exec_locals = {}
                exec(code, exec_globals, exec_locals)

                return {
                    "success": True,
                    "result": exec_locals.get("result", "Code executed successfully"),
                    "output": exec_locals,
                }

        except Exception as e:
            logger.error(f"Code execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
            }


class ToolRegistry:
    """Registry for managing tools."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

        # Register default tools
        self.register_tool(FileOperationsTool())
        self.register_tool(DataProcessingTool())
        self.register_tool(CodeExecutionTool())

        logger.info("Tool registry initialized with default tools")

    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a tool.

        Args:
            tool: Tool to register
        """
        self.tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance, or None if not found
        """
        return self.tools.get(name)

    def list_tools(self) -> list[Dict[str, str]]:
        """
        List all available tools.

        Returns:
            List of tool descriptions
        """
        return [tool.to_dict() for tool in self.tools.values()]

    def has_tool(self, name: str) -> bool:
        """
        Check if a tool exists.

        Args:
            name: Tool name

        Returns:
            True if tool exists
        """
        return name in self.tools
