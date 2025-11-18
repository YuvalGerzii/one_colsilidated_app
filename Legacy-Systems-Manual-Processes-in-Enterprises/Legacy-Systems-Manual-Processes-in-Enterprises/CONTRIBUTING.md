# Contributing to Enterprise AI Modernization Suite

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Prioritize the community's best interests

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/Legacy-Systems-Manual-Processes-in-Enterprises.git
   cd Legacy-Systems-Manual-Processes-in-Enterprises
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Style

We use the following tools:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Before committing, run:
```bash
black src/ tests/
ruff check src/ tests/
mypy src/
```

### Testing

Write tests for all new features:
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example:
```
feat: add support for Oracle database in legacy migrator

- Implement Oracle connector
- Add Oracle-specific code analysis
- Update documentation
```

## Pull Request Process

1. **Update documentation** for any new features
2. **Add tests** with >80% coverage
3. **Run the full test suite** and ensure it passes
4. **Update CHANGELOG.md** with your changes
5. **Submit PR** with clear description

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## Module Guidelines

When adding new modules:

1. **Create in appropriate directory** under `src/`
2. **Follow existing patterns**:
   - `models.py` - Pydantic models
   - `engine.py` or `service.py` - Business logic
   - API routes in `src/api/routes/`
3. **Add comprehensive tests**
4. **Update main README.md**

## Documentation

- Use Google-style docstrings
- Add type hints to all functions
- Update API documentation
- Include usage examples

Example:
```python
async def process_data(data: Dict[str, Any], options: Optional[ProcessOptions] = None) -> ProcessResult:
    """
    Process input data with specified options.

    Args:
        data: Input data dictionary
        options: Optional processing configuration

    Returns:
        ProcessResult: Processing results

    Raises:
        ValueError: If data is invalid
    """
    pass
```

## Issue Guidelines

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error logs/screenshots

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative approaches
- Additional context

## Community

- **Discussions**: Use GitHub Discussions for questions
- **Slack**: Join our community Slack (link in README)
- **Twitter**: Follow updates @EnterpriseAISuite

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

Feel free to ask questions by:
- Opening a GitHub Discussion
- Joining our Slack community
- Emailing: opensource@enterprise-ai-suite.com

Thank you for contributing! 🚀
