# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-12-27

### Added
- Initial project structure with modern Python packaging
- Core modules for compliance analysis:
  - `ingestion.py`: Load policy documents, questionnaires, and frameworks
  - `parsing.py`: Text parsing and normalization utilities
  - `questionnaire.py`: Questionnaire structures and scoring logic
  - `frameworks.py`: Framework mapping structures and loaders
  - `risk_report.py`: Risk report generation (CSV and JSON)
  - `utils.py`: File handling and logging utilities
- Command-line interface with subcommands:
  - `ingest`: Read inputs from existing data folders
  - `analyze`: Generate risk reports
  - `notebooks`: List and organize Jupyter notebooks
  - `info`: Display environment information
- Test suite with pytest:
  - CLI command tests
  - Parsing utility tests
  - Test fixtures and configuration
- CI/CD pipeline with GitHub Actions:
  - Multi-version Python testing (3.10, 3.11, 3.12)
  - Code quality checks (black, isort, flake8)
  - Automated test execution
  - Test result artifacts
- Development tooling:
  - `.gitignore` for Python projects
  - `.pre-commit-config.yaml` with formatting hooks
  - `setup.cfg` for tool configuration
  - `pyproject.toml` for modern packaging
  - `requirements.txt` for dependencies
- Containerization:
  - `Dockerfile` for building the application
  - `docker-compose.yml` for local development
- Comprehensive documentation:
  - Expanded `README.md` with installation and usage
  - `CONTRIBUTING.md` with development guidelines
  - `CODE_OF_CONDUCT.md` based on Contributor Covenant
  - `CHANGELOG.md` for version history
- Notebooks organization:
  - `notebooks/` directory structure
  - README with conventions and usage

### Changed
- Restructured repository from notebook-only to full Python project
- Preserved existing domain folders without modification

### Infrastructure
- GitHub Actions CI workflow for continuous integration
- Docker support for reproducible environments
- Pre-commit hooks for code quality

[Unreleased]: https://github.com/AnubhavPradhan/NexComply-analyser-/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AnubhavPradhan/NexComply-analyser-/releases/tag/v0.1.0
