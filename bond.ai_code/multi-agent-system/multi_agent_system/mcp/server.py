"""
Full Model Context Protocol (MCP) Server implementation.

Based on Anthropic's MCP specification for standardized agent communication.
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import asyncio


class ResourceType(Enum):
    """MCP resource types."""
    TEXT = "text"
    IMAGE = "image"
    BINARY = "binary"
    STRUCTURED = "structured"


class ToolCategory(Enum):
    """Tool categories."""
    FILE_OPERATIONS = "file_operations"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    COMPUTATION = "computation"
    EXTERNAL_API = "external_api"


@dataclass
class MCPResource:
    """An MCP resource (data accessible by agents)."""
    uri: str
    name: str
    description: str
    resource_type: ResourceType
    mime_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "type": self.resource_type.value,
            "mimeType": self.mime_type,
            "metadata": self.metadata,
        }


@dataclass
class MCPTool:
    """An MCP tool (capability exposed to agents)."""
    name: str
    description: str
    category: ToolCategory
    input_schema: Dict[str, Any]
    handler: Callable
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "inputSchema": self.input_schema,
            "metadata": self.metadata,
        }


@dataclass
class MCPPrompt:
    """An MCP prompt template."""
    name: str
    description: str
    template: str
    arguments: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "template": self.template,
            "arguments": self.arguments,
            "metadata": self.metadata,
        }

    def render(self, **kwargs) -> str:
        """Render prompt with arguments."""
        return self.template.format(**kwargs)


class MCPServer:
    """
    Model Context Protocol Server.

    Provides standardized interface for:
    - Resource management
    - Tool registration and execution
    - Prompt templates
    - Agent capabilities
    """

    def __init__(self, server_name: str = "multi-agent-mcp-server"):
        """
        Initialize MCP server.

        Args:
            server_name: Name of the MCP server
        """
        self.server_name = server_name
        self.server_version = "1.0.0"

        # MCP components
        self.resources: Dict[str, MCPResource] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.prompts: Dict[str, MCPPrompt] = {}

        # Resource handlers (URI -> handler function)
        self.resource_handlers: Dict[str, Callable] = {}

        # Server capabilities
        self.capabilities = {
            "resources": True,
            "tools": True,
            "prompts": True,
            "sampling": True,
        }

        logger.info(f"MCP Server '{server_name}' initialized")

    # ===== Resource Management =====

    def register_resource(
        self,
        uri: str,
        name: str,
        description: str,
        resource_type: ResourceType,
        handler: Callable,
        mime_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Register a resource.

        Args:
            uri: Resource URI (e.g., "file://data/knowledge.txt")
            name: Human-readable name
            description: Resource description
            resource_type: Type of resource
            handler: Function to retrieve resource content
            mime_type: MIME type (optional)
            metadata: Additional metadata
        """
        resource = MCPResource(
            uri=uri,
            name=name,
            description=description,
            resource_type=resource_type,
            mime_type=mime_type,
            metadata=metadata or {},
        )

        self.resources[uri] = resource
        self.resource_handlers[uri] = handler

        logger.info(f"Registered resource: {uri}")

    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a resource by URI.

        Args:
            uri: Resource URI

        Returns:
            Resource content and metadata

        Raises:
            ValueError: If resource not found
        """
        if uri not in self.resources:
            raise ValueError(f"Resource not found: {uri}")

        resource = self.resources[uri]
        handler = self.resource_handlers[uri]

        # Execute handler to get content
        if asyncio.iscoroutinefunction(handler):
            content = await handler()
        else:
            content = handler()

        return {
            "uri": uri,
            "content": content,
            "mimeType": resource.mime_type,
            "metadata": resource.metadata,
        }

    def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources."""
        return [resource.to_dict() for resource in self.resources.values()]

    # ===== Tool Management =====

    def register_tool(
        self,
        name: str,
        description: str,
        category: ToolCategory,
        input_schema: Dict[str, Any],
        handler: Callable,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Register a tool.

        Args:
            name: Tool name
            description: Tool description
            category: Tool category
            input_schema: JSON schema for tool inputs
            handler: Function to execute tool
            metadata: Additional metadata
        """
        tool = MCPTool(
            name=name,
            description=description,
            category=category,
            input_schema=input_schema,
            handler=handler,
            metadata=metadata or {},
        )

        self.tools[name] = tool

        logger.info(f"Registered tool: {name}")

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
        """
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")

        tool = self.tools[name]

        logger.debug(f"Calling tool: {name}")

        # Execute tool handler
        if asyncio.iscoroutinefunction(tool.handler):
            result = await tool.handler(**arguments)
        else:
            result = tool.handler(**arguments)

        return result

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        return [tool.to_dict() for tool in self.tools.values()]

    # ===== Prompt Management =====

    def register_prompt(
        self,
        name: str,
        description: str,
        template: str,
        arguments: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Register a prompt template.

        Args:
            name: Prompt name
            description: Prompt description
            template: Prompt template with {placeholders}
            arguments: List of argument definitions
            metadata: Additional metadata
        """
        prompt = MCPPrompt(
            name=name,
            description=description,
            template=template,
            arguments=arguments or [],
            metadata=metadata or {},
        )

        self.prompts[name] = prompt

        logger.info(f"Registered prompt: {name}")

    def get_prompt(self, name: str, **kwargs) -> str:
        """
        Get and render a prompt.

        Args:
            name: Prompt name
            **kwargs: Arguments to render prompt

        Returns:
            Rendered prompt

        Raises:
            ValueError: If prompt not found
        """
        if name not in self.prompts:
            raise ValueError(f"Prompt not found: {name}")

        prompt = self.prompts[name]
        return prompt.render(**kwargs)

    def list_prompts(self) -> List[Dict[str, Any]]:
        """List all available prompts."""
        return [prompt.to_dict() for prompt in self.prompts.values()]

    # ===== Server Information =====

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return {
            "name": self.server_name,
            "version": self.server_version,
            "capabilities": self.capabilities,
            "resourceCount": len(self.resources),
            "toolCount": len(self.tools),
            "promptCount": len(self.prompts),
        }

    # ===== Sampling Support =====

    async def create_message(
        self,
        messages: List[Dict[str, Any]],
        model_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a message using MCP sampling.

        This allows the server to request LLM sampling on behalf of clients.

        Args:
            messages: Message history
            model_preferences: Model preferences (temperature, etc.)

        Returns:
            Generated message
        """
        # This would integrate with an actual LLM
        # For now, return a placeholder
        logger.info("MCP sampling requested")

        return {
            "role": "assistant",
            "content": "MCP sampling response (placeholder)",
            "model": model_preferences.get("model", "default") if model_preferences else "default",
        }


class MCPClient:
    """
    Model Context Protocol Client.

    Connects to MCP servers and uses their capabilities.
    """

    def __init__(self, client_name: str = "multi-agent-mcp-client"):
        """
        Initialize MCP client.

        Args:
            client_name: Name of the MCP client
        """
        self.client_name = client_name
        self.connected_servers: Dict[str, MCPServer] = {}

        logger.info(f"MCP Client '{client_name}' initialized")

    def connect_server(self, server_name: str, server: MCPServer) -> None:
        """
        Connect to an MCP server.

        Args:
            server_name: Name to refer to this server
            server: MCP server instance
        """
        self.connected_servers[server_name] = server
        logger.info(f"Connected to MCP server: {server_name}")

    async def list_resources(self, server_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List resources from connected server(s).

        Args:
            server_name: Specific server, or None for all servers

        Returns:
            List of available resources
        """
        if server_name:
            if server_name not in self.connected_servers:
                raise ValueError(f"Not connected to server: {server_name}")
            return self.connected_servers[server_name].list_resources()

        # List from all servers
        all_resources = []
        for name, server in self.connected_servers.items():
            resources = server.list_resources()
            for resource in resources:
                resource["server"] = name
            all_resources.extend(resources)

        return all_resources

    async def read_resource(self, uri: str, server_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Read a resource.

        Args:
            uri: Resource URI
            server_name: Server to read from (optional)

        Returns:
            Resource content
        """
        if server_name:
            if server_name not in self.connected_servers:
                raise ValueError(f"Not connected to server: {server_name}")
            return await self.connected_servers[server_name].read_resource(uri)

        # Try all servers
        for server in self.connected_servers.values():
            try:
                return await server.read_resource(uri)
            except ValueError:
                continue

        raise ValueError(f"Resource not found: {uri}")

    async def list_tools(self, server_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """List tools from connected server(s)."""
        if server_name:
            if server_name not in self.connected_servers:
                raise ValueError(f"Not connected to server: {server_name}")
            return self.connected_servers[server_name].list_tools()

        # List from all servers
        all_tools = []
        for name, server in self.connected_servers.items():
            tools = server.list_tools()
            for tool in tools:
                tool["server"] = name
            all_tools.extend(tools)

        return all_tools

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        server_name: Optional[str] = None,
    ) -> Any:
        """
        Call a tool.

        Args:
            tool_name: Tool name
            arguments: Tool arguments
            server_name: Server to use (optional)

        Returns:
            Tool result
        """
        if server_name:
            if server_name not in self.connected_servers:
                raise ValueError(f"Not connected to server: {server_name}")
            return await self.connected_servers[server_name].call_tool(tool_name, arguments)

        # Try all servers
        for server in self.connected_servers.values():
            try:
                return await server.call_tool(tool_name, arguments)
            except ValueError:
                continue

        raise ValueError(f"Tool not found: {tool_name}")

    def get_prompt(self, prompt_name: str, server_name: Optional[str] = None, **kwargs) -> str:
        """Get and render a prompt template."""
        if server_name:
            if server_name not in self.connected_servers:
                raise ValueError(f"Not connected to server: {server_name}")
            return self.connected_servers[server_name].get_prompt(prompt_name, **kwargs)

        # Try all servers
        for server in self.connected_servers.values():
            try:
                return server.get_prompt(prompt_name, **kwargs)
            except ValueError:
                continue

        raise ValueError(f"Prompt not found: {prompt_name}")
