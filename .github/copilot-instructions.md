# Copilot Instructions for NexComply-analyser

## Repository Overview

This repository contains compliance and GRC (Governance, Risk, and Compliance) analysis tools and documentation for NexComply. The primary purpose is to analyze security posture, manage compliance frameworks, and maintain policy documentation.

## Repository Structure

- **First Session/** and **Second Session/**: Jupyter notebooks for security policy analysis
- **Frameworks/**: Security framework assessment spreadsheets
- **Questionnaires/**: Compliance questionnaires in Excel format
- **New Format Policy Docs/**: Standardized policy documents (PDF format)
- **Risk Reports/**: Vulnerability assessment and third-party risk management reports
- **Session on GRC/**: Training materials and presentations on GRC fundamentals
- **Dummy KL/**: Knowledge library samples

## Technology Stack

- **Python**: Primary language for analysis notebooks
- **Jupyter Notebooks**: Interactive analysis and documentation
- **Excel**: Framework assessments and questionnaires
- **PDF/Word Documents**: Policy documentation and reports

## Coding Guidelines

### Jupyter Notebooks
- Use clear cell comments to explain analysis steps
- Include markdown cells for section headers and explanations
- Follow data analysis best practices with pandas, numpy
- Always include proper error handling for data loading
- Document data sources and assumptions
- Keep notebook output cells to show analysis results

### Python Code
- Follow PEP 8 style guidelines
- Use descriptive variable names that reflect compliance/GRC terminology
- Add docstrings to functions explaining their purpose in the context of compliance analysis
- Handle missing data gracefully
- Use type hints where appropriate

### Documentation
- Policy documents should follow a consistent structure
- Use clear headings and sections
- Include document version and last updated date
- Maintain professional compliance language
- Reference relevant frameworks (ISO 27001, NIST, SOC 2, etc.) where applicable

## Domain-Specific Guidelines

### Compliance Analysis
- When analyzing frameworks, ensure control mappings align with the specific requirements of each framework (e.g., ISO 27001 Annex A controls, NIST CSF subcategories, SOC 2 trust service criteria)
- Consider multiple compliance frameworks (ISO 27001, SOC 2, NIST CSF, etc.)
- Document control mappings clearly with traceability to framework requirements
- Include risk ratings and justifications

### Policy Management
- Policies should be versioned
- Include effective dates and review cycles
- Reference applicable regulations and standards
- Maintain consistent terminology across policies

### Risk Assessment
- Use standardized risk scoring methodologies such as quantitative approaches (FAIR, OCTAVE) or qualitative scales (High/Medium/Low with clearly defined criteria)
- Document risk assessment criteria including likelihood and impact definitions
- Include mitigation recommendations
- Track remediation timelines

### GRC Best Practices
- Maintain traceability between controls and requirements
- Document exceptions and compensating controls
- Keep evidence collection processes consistent
- Ensure audit-ready documentation

## File Naming Conventions

- Use descriptive names that indicate content and purpose
- Include version numbers or dates where relevant
- Use spaces in folder names as per existing structure
- Policy documents: Use descriptive names with policy type

## Working with This Repository

### When Modifying Notebooks
- Test all code cells before committing
- Ensure data file paths are relative or configurable using environment variables or configuration files (e.g., `DATA_DIR` environment variable or `config.yaml`)
- Clear sensitive data from outputs before committing
- Update markdown explanations if logic changes

### When Adding Documents
- Place in appropriate directory based on content type
- Follow existing naming patterns
- Ensure documents are in final/published format
- Update README if adding new content categories

### When Creating Analysis Scripts
- Focus on reusability across different frameworks
- Parameterize inputs for different compliance standards
- Output results in formats suitable for reporting
- Include data validation steps

## Security Considerations

- Never commit sensitive compliance data or actual company information
- Use anonymized or sample data in examples
- Redact PII and confidential information from reports
- Follow data privacy regulations (GDPR, CCPA) in analysis

## Dependencies

When adding new Python dependencies:
- Document why the dependency is needed
- Prefer well-maintained, security-focused libraries
- Create or update requirements.txt
- Consider compatibility with Jupyter environment

## Testing

- Test notebook cells in order from top to bottom
- Verify analysis produces expected output formats
- Validate data transformations with sample data
- Check document formatting and readability

## Contribution Guidelines

- Keep changes focused on compliance/GRC domain
- Maintain professional documentation standards
- Ensure changes don't break existing analyses
- Update documentation to reflect changes
- Follow existing directory structure
