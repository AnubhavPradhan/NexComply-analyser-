# 🛡️ NexComply Analyzer

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Enterprise-grade GRC (Governance, Risk & Compliance) automation platform with RAG capabilities, advanced risk assessment, and comprehensive web interface.**

## 🌟 Features

### Core Capabilities

- **🤖 RAG-Enhanced Compliance Analysis**
  - Semantic search across compliance frameworks using ChromaDB
  - Automated gap identification and severity assessment
  - Context-aware recommendations powered by sentence transformers
  - Support for multiple document formats (PDF, DOCX, TXT)

- **⚠️ Advanced Risk Assessment**
  - Multi-factor risk analysis with 5x5 matrix
  - Inherent vs. residual risk calculation
  - Control effectiveness evaluation
  - Risk velocity tracking and trending
  - Automated mitigation recommendations

- **📚 Framework Support**
  - ISO 27001
  - NIST Cybersecurity Framework
  - SOC 2
  - GDPR
  - HIPAA
  - PCI-DSS
  - CIS Controls
  - COBIT
  - ITIL

- **🎯 Interactive Dashboard**
  - Real-time compliance KPIs and metrics
  - Risk distribution visualizations
  - Framework explorer with search
  - Report generation in multiple formats
  - Configuration management

- **🚀 RESTful API**
  - FastAPI-based endpoints
  - OpenAPI documentation
  - Asynchronous processing
  - Health monitoring

## 🏗️ Architecture

```
nexcomply-analyzer/
├── src/
│   ├── config/          # Configuration management
│   ├── models/          # Core ML models (RAG, Risk Assessor)
│   ├── data/            # Data loaders and processors
│   ├── api/             # FastAPI routes and schemas
│   └── utils/           # Utilities (embeddings, reporting)
├── tests/               # Unit and integration tests
├── docker/              # Docker configuration
├── streamlit_app.py     # Interactive dashboard
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (optional)
- 8GB+ RAM recommended
- OpenAI API key (optional, for enhanced features)

### Installation

#### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/AnubhavPradhan/NexComply-analyser-.git
cd NexComply-analyser-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

#### Option 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/AnubhavPradhan/NexComply-analyser-.git
cd NexComply-analyser-

# Build and run with Docker Compose
docker-compose -f docker/docker-compose.yml up -d
```

### Running the Application

#### Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Access the dashboard at: http://localhost:8501

#### FastAPI Server

```bash
uvicorn src.api.routes:app --host 0.0.0.0 --port 8000
```

Access the API docs at: http://localhost:8000/docs

## 📖 Usage Examples

### 1. Compliance Gap Analysis

```python
from src.models.compliance_analyzer import RAGComplianceAnalyzer
from src.data.framework_loader import FrameworkLoader
from src.data.policy_processor import PolicyProcessor

# Initialize components
analyzer = RAGComplianceAnalyzer(
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
    vector_db_path="./data/vector_db"
)

framework_loader = FrameworkLoader()
policy_processor = PolicyProcessor()

# Load framework
controls = framework_loader.load_framework("ISO27001")
analyzer.index_framework("ISO27001", controls)

# Load policy document
policy_text = policy_processor.load_document("path/to/policy.pdf")

# Analyze gaps
gaps = analyzer.analyze_compliance_gap(
    framework="ISO27001",
    policy_document=policy_text,
    top_k=5
)

# Print results
for gap in gaps:
    print(f"Control: {gap['control_id']}")
    print(f"Severity: {gap['severity']}")
    print(f"Recommendations: {gap['recommendations']}")
    print("---")
```

### 2. Risk Assessment

```python
from src.models.risk_assessor import AdvancedRiskAssessor, RiskFactor

# Initialize assessor
assessor = AdvancedRiskAssessor()

# Define risk factors
risk_factors = [
    RiskFactor(
        name="Data Breach",
        category="Technical",
        likelihood=4,
        impact=5,
        current_controls="Encryption, Access Controls",
        control_effectiveness=60.0
    ),
    RiskFactor(
        name="Insider Threat",
        category="Operational",
        likelihood=3,
        impact=4,
        current_controls="Background Checks, Monitoring",
        control_effectiveness=50.0
    )
]

# Perform assessment
assessment = assessor.assess_risk(
    risk_factors=risk_factors,
    risk_id="RISK-001",
    description="Security risk assessment"
)

print(f"Inherent Risk: {assessment.inherent_risk_score}")
print(f"Residual Risk: {assessment.residual_risk_score}")
print(f"Risk Level: {assessment.risk_level}")
print(f"Recommendations: {assessment.recommendations}")
```

### 3. API Usage

```bash
# Health check
curl http://localhost:8000/health

# List frameworks
curl http://localhost:8000/api/v1/frameworks

# Analyze compliance
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "ISO27001",
    "policy_document": "Your policy text here...",
    "top_k": 5
  }'

# Assess risk
curl -X POST http://localhost:8000/api/v1/assess-risk \
  -H "Content-Type: application/json" \
  -d '{
    "risk_id": "RISK-001",
    "description": "Test risk",
    "risk_factors": [
      {
        "name": "Test Factor",
        "category": "Technical",
        "likelihood": 3,
        "impact": 4,
        "current_controls": "Test controls",
        "control_effectiveness": 50.0
      }
    ]
  }'
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v
```

## 📊 Supported Frameworks

| Framework | Version | Controls | Status |
|-----------|---------|----------|--------|
| ISO 27001 | 2022 | 93 | ✅ Supported |
| NIST CSF | 1.1 | 108 | ✅ Supported |
| SOC 2 | 2017 | 64 | ✅ Supported |
| GDPR | 2018 | 99 | ✅ Supported |
| HIPAA | 2013 | 45 | ✅ Supported |
| PCI-DSS | 4.0 | 362 | ✅ Supported |
| CIS Controls | v8 | 153 | ✅ Supported |
| COBIT | 2019 | 40 | ✅ Supported |
| ITIL | v4 | 34 | ✅ Supported |

## ⚙️ Configuration

Key configuration options in `.env`:

```env
# API Keys
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///./nexcomply.db
VECTOR_DB_PATH=./data/vector_db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Model Settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo

# Processing
WORKERS=4
BATCH_SIZE=32
```

## 🐳 Docker Deployment

The application includes Docker support for easy deployment:

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

Services:
- **nexcomply-api**: FastAPI server on port 8000
- **nexcomply-dashboard**: Streamlit dashboard on port 8501
- **postgres**: PostgreSQL database on port 5432

## 📚 API Documentation

Once the API server is running, visit:
- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

- `GET /health` - Health check
- `GET /api/v1/frameworks` - List available frameworks
- `POST /api/v1/analyze` - Analyze compliance gaps
- `POST /api/v1/assess-risk` - Perform risk assessment
- `POST /api/v1/search` - Semantic search

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings (Google style)
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

- [ ] Machine learning model fine-tuning
- [ ] Integration with ticketing systems (Jira, ServiceNow)
- [ ] Real-time notifications (Slack, Teams)
- [ ] Advanced analytics and reporting
- [ ] Multi-tenant support
- [ ] Mobile application
- [ ] AI-powered control recommendations
- [ ] Automated evidence collection
- [ ] Continuous compliance monitoring

## 👥 Authors

- **NexComply Team** - *Initial work*

## 🙏 Acknowledgments

- OpenAI for GPT models
- Sentence Transformers for embedding models
- ChromaDB for vector storage
- Streamlit for the dashboard framework
- FastAPI for the API framework

## 📞 Support

For support, please open an issue on GitHub or contact us at info@nexcomply.com

---

**Built with ❤️ for the GRC community**