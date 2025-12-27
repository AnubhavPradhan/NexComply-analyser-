# Notebooks

This directory contains Jupyter notebooks for exploratory analysis and demonstrations of NexComply Analyser functionality.

## Organization

Notebooks are organized by topic or analysis type:

- **exploratory/**: Initial data exploration and analysis
- **examples/**: Usage examples and tutorials
- **reports/**: Analysis reports and visualizations

## Running Notebooks

### Prerequisites

Install Jupyter and required dependencies:

```bash
# Install the project in development mode
pip install -e ".[dev]"

# Install Jupyter
pip install jupyter notebook jupyterlab
```

### Starting Jupyter

```bash
# Start Jupyter Notebook
jupyter notebook

# Or start JupyterLab
jupyter lab
```

### Using the CLI to Organize Notebooks

The `nexcomply-analyser notebooks` command helps manage notebooks:

```bash
# List all notebooks in the repository
nexcomply-analyser notebooks

# Copy notebooks to this directory
nexcomply-analyser notebooks --copy
```

## Conventions

### Naming

Use descriptive names with prefixes:
- `01_`: Introduction or setup
- `02_`, `03_`, etc.: Sequential analyses
- `explore_`: Exploratory analysis
- `example_`: Usage examples
- `report_`: Final reports

Examples:
- `01_data_ingestion_intro.ipynb`
- `explore_policy_documents.ipynb`
- `example_risk_scoring.ipynb`

### Structure

Each notebook should include:

1. **Title and Description**: Clear explanation of purpose
2. **Setup**: Import statements and configuration
3. **Analysis**: Main content with clear sections
4. **Conclusions**: Summary of findings
5. **Next Steps**: Follow-up questions or analyses

### Code Style

- Follow the same code style as the main project
- Add comments for complex operations
- Clear markdown explanations between code cells
- Use meaningful variable names

### Best Practices

- **Keep notebooks focused**: One main topic per notebook
- **Clear outputs**: Ensure visualizations are readable
- **Reproducible**: Set random seeds, document dependencies
- **Clean execution**: Restart kernel and run all cells before committing
- **Version control**: Clear outputs before committing large notebooks

## Environment

The notebooks have access to the full NexComply Analyser package:

```python
from nexcomply_analyser.ingestion import DataIngestion
from nexcomply_analyser.risk_report import RiskReportGenerator
from nexcomply_analyser.frameworks import FrameworkLoader

# Example: Load data
ingestion = DataIngestion()
data = ingestion.ingest_all()
```

## Examples

See existing notebooks in the repository:
- `First Session/secpal.ipynb`: Original security policy analysis
- `Second Session/secpal2.ipynb`: Extended security policy analysis

## Contributing

When adding new notebooks:

1. Place them in an appropriate subdirectory
2. Follow naming conventions
3. Include clear documentation
4. Test execution from start to finish
5. Consider adding corresponding tests in `tests/`

## Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [Project Documentation](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
