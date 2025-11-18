# Contributing to Multi-Agent System

Thank you for your interest in contributing to the Multi-Agent System project!

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Code Contributions

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python tests/test_basic.py
   python examples/basic_usage.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions/classes
- Keep functions focused and modular

## Testing

- Add tests for new features
- Ensure all existing tests pass
- Test with different configurations

## Documentation

- Update README.md if needed
- Add docstrings to new code
- Create examples for new features
- Update CHANGELOG.md

## Custom Agents

When creating custom agents:

1. Inherit from `BaseAgent`
2. Implement `process_task` method
3. Define appropriate capabilities
4. Add docstrings and examples
5. Test thoroughly

Example:
```python
from multi_agent_system import BaseAgent, AgentCapability

class MyAgent(BaseAgent):
    def __init__(self, agent_id="my_agent", message_bus=None):
        capabilities = [
            AgentCapability("my_capability", "Description", 0.9)
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task):
        # Your implementation
        pass
```

## Questions?

Feel free to open an issue for any questions or clarifications.

Thank you for contributing!
