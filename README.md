# NexComply Analyser

A modern Python tool for analyzing compliance frameworks, questionnaires, and risk reports in GRC (Governance, Risk, and Compliance) activities.

## Overview

NexComply Analyser provides a structured approach to:
- Ingest and analyze policy documents, questionnaires, and compliance frameworks
- Generate risk reports in CSV and JSON formats
- Organize and manage compliance data
- Support reproducible analysis workflows

The tool transforms raw compliance data into actionable insights while maintaining a clean, maintainable codebase.

## Features

- 📊 **Data Ingestion**: Load policy documents, questionnaires, and frameworks from various formats
- 📈 **Risk Analysis**: Generate comprehensive risk reports with scoring
- 🖥️ **CLI Interface**: Easy-to-use command-line interface with multiple commands
- 🧪 **Testing**: Full test suite with pytest
- 🐳 **Containerization**: Docker support for consistent environments
- 🔄 **CI/CD**: GitHub Actions workflow for automated testing and linting

## Installation

### Using pip (recommended)

```bash
# Clone the repository
git clone https://github.com/AnubhavPradhan/NexComply-analyser-.git
cd NexComply-analyser-

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# For development with all tools
pip install -e ".[dev]"
```

### Using Docker

```bash
# Build the Docker image
docker build -t nexcomply-analyser .

# Run using docker-compose
docker-compose up
```

## Quick Start

### Command Line Interface

The tool provides several commands:

```bash
# Show version and help
nexcomply-analyser --version
nexcomply-analyser --help

# Display environment information
nexcomply-analyser info

# Ingest data from existing folders
nexcomply-analyser ingest

# Generate risk analysis reports
nexcomply-analyser analyze

# List and organize notebooks
nexcomply-analyser notebooks
nexcomply-analyser notebooks --copy  # Copy to notebooks/ directory
```

### Basic Usage Example

```bash
# 1. Ingest data from the data folders
nexcomply-analyser ingest --verbose

# 2. Generate risk reports
nexcomply-analyser analyze

# Reports will be created in the "Risk Reports/" directory:
# - risk_report_YYYYMMDD_HHMMSS.csv
# - risk_report_YYYYMMDD_HHMMSS.json
```

### Using as a Python Library

```python
from nexcomply_analyser.ingestion import DataIngestion
from nexcomply_analyser.risk_report import RiskReportGenerator

# Ingest data
ingestion = DataIngestion()
data = ingestion.ingest_all()

# Generate reports
generator = RiskReportGenerator()
reports = generator.generate_reports()

print(f"CSV Report: {reports['csv']}")
print(f"JSON Report: {reports['json']}")
```

## Project Structure

```
NexComply-analyser-/
├── src/nexcomply_analyser/      # Main package
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Command-line interface
│   ├── ingestion.py             # Data ingestion logic
│   ├── parsing.py               # Text parsing utilities
│   ├── questionnaire.py         # Questionnaire structures
│   ├── frameworks.py            # Framework mappings
│   ├── risk_report.py           # Report generation
│   └── utils.py                 # Utility functions
├── tests/                       # Test suite
│   ├── conftest.py              # Test fixtures
│   ├── test_cli.py              # CLI tests
│   └── test_parsing.py          # Parsing tests
├── notebooks/                   # Jupyter notebooks
├── .github/workflows/           # CI/CD workflows
│   └── ci.yml                   # GitHub Actions CI
├── Dummy KL/                    # Data: Knowledge Library
├── Frameworks/                  # Data: Compliance frameworks
├── New Format Policy Docs/      # Data: Policy documents
├── Questionnaires/              # Data: Questionnaires
├── Risk Reports/                # Output: Generated reports
├── Session on GRC/              # Data: GRC sessions
├── First Session/               # Data: Training materials
├── Second Session/              # Data: Training materials
├── pyproject.toml               # Project configuration
├── setup.cfg                    # Tool configuration
├── requirements.txt             # Dependencies
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Docker orchestration
├── .gitignore                   # Git ignore rules
├── .pre-commit-config.yaml      # Pre-commit hooks
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Code of conduct
└── README.md                    # This file
```

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nexcomply_analyser --cov-report=html

# Run specific test file
pytest tests/test_cli.py -v
```

### Code Quality

```bash
# Format code with black
black src/ scripts/ tests/

# Sort imports with isort
isort src/ scripts/ tests/

# Lint with flake8
flake8 src/ scripts/ tests/

# Run all checks (pre-commit)
pre-commit run --all-files
```

### Building Documentation

The project uses inline documentation. To generate API docs:

```bash
# Using pdoc (install with: pip install pdoc)
pdoc nexcomply_analyser --html --output-dir docs
```

## CI/CD

The project uses GitHub Actions for continuous integration:

- **Automated Testing**: Runs tests on Python 3.10, 3.11, and 3.12
- **Code Quality**: Checks formatting (black), imports (isort), and linting (flake8)
- **Test Reports**: Uploads test results as artifacts

The CI workflow runs on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please:
- Open an issue on [GitHub Issues](https://github.com/AnubhavPradhan/NexComply-analyser-/issues)
- Review existing [documentation](README.md)
- Check the [CHANGELOG](CHANGELOG.md) for recent updates

## Versioning

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality (backward compatible)
- **PATCH** version for bug fixes (backward compatible)

Current version: **0.1.0** (Alpha)

## Acknowledgments

- Built for GRC compliance analysis and risk management
- Supports ISO 27001, SOC 2, NIST, GDPR, HIPAA, and PCI DSS frameworks
- Designed for extensibility and maintainability