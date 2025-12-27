# Contributing to NexComply Analyser

Thank you for your interest in contributing to NexComply Analyser! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Code samples** or error messages if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** explaining why this would be useful
- **Possible implementation** if you have ideas
- **Examples** from other projects if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Update documentation** if you've changed APIs or functionality
5. **Run the test suite** and ensure all tests pass
6. **Run linters** and fix any issues
7. **Commit your changes** with clear commit messages
8. **Push to your fork** and submit a pull request

## Development Setup

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Git
- pip or another package manager

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/NexComply-analyser-.git
cd NexComply-analyser-

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (enforced by Black)
- **Imports**: Sorted using isort with Black profile
- **Type hints**: Use type hints for function signatures
- **Docstrings**: Use Google-style docstrings

### Code Formatting

We use automated tools to maintain consistent code style:

```bash
# Format code with Black
black src/ scripts/ tests/

# Sort imports with isort
isort src/ scripts/ tests/

# Check with flake8
flake8 src/ scripts/ tests/
```

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed explaining the function's
    purpose and behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=nexcomply_analyser --cov-report=html

# Run specific test file
pytest tests/test_cli.py -v

# Run specific test
pytest tests/test_cli.py::test_cli_help -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Name test functions with `test_` prefix
- Use fixtures from `conftest.py` for common setup
- Aim for high test coverage (>80%)

Example test:

```python
def test_function_name():
    """Test that function_name works correctly."""
    result = function_name("input")
    assert result == "expected_output"
```

## Commit Messages

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

Good examples:
```
Add questionnaire scoring functionality
Fix issue with empty policy documents (#123)
Update README with installation instructions
```

## Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Ensure CI passes** - all tests and linters must pass
4. **Update CHANGELOG.md** with your changes
5. **Request review** from maintainers
6. **Address feedback** promptly and professionally

### PR Title Format

Use clear, descriptive titles:
- `feat: Add new risk scoring algorithm`
- `fix: Correct CSV export formatting`
- `docs: Update contribution guidelines`
- `test: Add tests for parsing module`
- `refactor: Simplify ingestion logic`

## Project Structure

Key directories and their purposes:

- `src/nexcomply_analyser/`: Main package code
- `scripts/`: CLI and utility scripts
- `tests/`: Test suite
- `notebooks/`: Jupyter notebooks for analysis
- `.github/workflows/`: CI/CD workflows

## Dependencies

### Adding Dependencies

When adding new dependencies:

1. Add to `pyproject.toml` under `dependencies` or `optional-dependencies`
2. Update `requirements.txt` if it's a runtime dependency
3. Explain why the dependency is needed in your PR
4. Prefer well-maintained, popular packages

### Dependency Guidelines

- Minimize external dependencies
- Use standard library when possible
- Pin major versions but allow minor updates
- Check for security vulnerabilities

## Code Review Process

All submissions require review. We aim to:

- Provide feedback within 48 hours
- Be respectful and constructive
- Focus on code quality and maintainability
- Ensure consistency with project standards

As a contributor, please:

- Be responsive to feedback
- Ask questions if feedback is unclear
- Be patient during the review process
- Learn from the feedback

## Getting Help

If you need help:

1. Check the [README](README.md) for basic information
2. Search [existing issues](https://github.com/AnubhavPradhan/NexComply-analyser-/issues)
3. Ask in your pull request or issue
4. Reach out to maintainers

## Recognition

Contributors are recognized in:

- CHANGELOG.md for significant contributions
- Project documentation
- Release notes

Thank you for contributing to NexComply Analyser!
