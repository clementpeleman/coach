# Contributing to Health Coach AI System

We're excited that you're interested in contributing to the Health Coach AI System! This document provides guidelines and information for contributors.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Guidelines](#code-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Reporting](#issue-reporting)
- [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Docker and Docker Compose (for full development environment)
- Basic understanding of AI/ML concepts
- Familiarity with Agno framework

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/health-coach-ai.git
   cd health-coach-ai
   ```

2. **Set up Development Environment**
   ```bash
   make setup
   source .venv/bin/activate
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Initialize Database**
   ```bash
   make db-init
   ```

5. **Run Tests**
   ```bash
   make test
   ```

6. **Start Development Server**
   ```bash
   make dev
   ```

## Code Guidelines

### Python Code Style
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Formatting
We use automated code formatting tools:
```bash
make format  # Formats code with black and isort
make lint    # Runs linting checks
```

### Agent Development Guidelines

#### Creating New Agents
1. **Inherit from Base Patterns**
   ```python
   from agno.agent import Agent
   from config.models.model_config import ModelConfig

   class MySpecializedAgent:
       def __init__(self, knowledge_base=None):
           self.agent = Agent(
               name="My Specialized Agent",
               model=ModelConfig.get_model_for_agent("my_agent"),
               description="Clear description of agent purpose",
               instructions="Detailed instructions for the agent"
           )
   ```

2. **Follow Naming Conventions**
   - Agent files: `snake_case.py`
   - Agent classes: `PascalCaseAgent`
   - Methods: `snake_case`

3. **Include Comprehensive Documentation**
   ```python
   class MyAgent:
       """
       Brief description of the agent's purpose.

       Capabilities:
       - List specific capabilities
       - Include key responsibilities
       - Mention any limitations

       Usage:
       - When to use this agent
       - How it integrates with other agents
       """
   ```

#### Agent Best Practices
- **Single Responsibility**: Each agent should have a clear, focused purpose
- **Stateless Design**: Agents should not maintain state between conversations
- **Error Handling**: Implement robust error handling and fallback strategies
- **Performance**: Consider response time and cost optimization
- **Testing**: Include comprehensive unit and integration tests

### Database Guidelines

#### Model Design
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MyModel(Base):
    __tablename__ = "my_models"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Include comprehensive documentation
```

#### Migration Best Practices
- Always create migrations for schema changes
- Test migrations on development data
- Include rollback procedures
- Document breaking changes

### Testing Guidelines

#### Test Structure
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for component interactions
├── agents/         # Agent-specific tests
├── workflows/      # Workflow tests
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

#### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch

class TestMyAgent:
    @pytest.fixture
    def my_agent(self):
        return MyAgent()

    @pytest.mark.unit
    async def test_agent_functionality(self, my_agent):
        # Test implementation
        pass

    @pytest.mark.integration
    async def test_agent_integration(self, my_agent):
        # Integration test implementation
        pass
```

#### Test Categories
- `@pytest.mark.unit`: Fast, isolated tests
- `@pytest.mark.integration`: Tests with external dependencies
- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.real_api`: Tests requiring real API connections

## Testing

### Running Tests
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test categories
make test-unit
make test-integration
make test-agents

# Run tests in watch mode
make test-watch
```

### Test Requirements
- **Coverage**: Maintain minimum 80% code coverage
- **Speed**: Unit tests should complete in under 1 second
- **Isolation**: Tests should not depend on external services (use mocks)
- **Reliability**: Tests should be deterministic and not flaky

## Submitting Changes

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow code guidelines
   - Add tests for new functionality
   - Update documentation

3. **Quality Checks**
   ```bash
   make quality  # Runs format, lint, and test
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new specialized agent for X"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines
Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

Examples:
```
feat: add nutrition tracking agent
fix: resolve Garmin API authentication issue
docs: update agent development guidelines
test: add integration tests for training planner
```

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Self-review of the code completed
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow conventions

## Issue Reporting

### Bug Reports
Use the bug report template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- System information (OS, Python version, etc.)
- Relevant logs or error messages

### Feature Requests
Use the feature request template and include:
- Clear description of the proposed feature
- Use case and motivation
- Possible implementation approaches
- Impact on existing functionality

### Security Issues
For security vulnerabilities:
- **DO NOT** create a public issue
- Email security concerns privately
- Include detailed description and impact assessment

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Communication
- **GitHub Discussions**: General questions and discussions
- **Issues**: Bug reports and feature requests
- **Discord**: Real-time community chat
- **Email**: Private or security-related communications

### Recognition
Contributors are recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- Release notes for major features

## Development Areas

### High Priority
- Agent performance optimization
- Enhanced health analytics
- Real-time data processing
- Mobile app integration

### Medium Priority
- Additional language support
- Social features
- Advanced visualization
- Third-party integrations

### Getting Started Areas
- Documentation improvements
- Test coverage expansion
- Bug fixes and small features
- Code refactoring and optimization

## Resources

### Documentation
- [Agno Framework Docs](https://docs.agno.com)
- [Project README](README.md)
- [API Documentation](docs/api/)
- [Agent Development Guide](docs/agents/)

### Learning Resources
- [AI Agent Patterns](docs/patterns/)
- [Health Coaching Principles](docs/health/)
- [System Architecture](docs/architecture/)

## Questions?

If you have questions:
1. Check existing documentation
2. Search GitHub issues
3. Ask in GitHub Discussions
4. Join our Discord community

Thank you for contributing to the Health Coach AI System! 🚀