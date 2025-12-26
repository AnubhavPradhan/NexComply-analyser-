"""
NexComply Analyzer - Enterprise GRC Automation Platform
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nexcomply-analyzer",
    version="1.0.0",
    author="NexComply Team",
    author_email="info@nexcomply.com",
    description="Enterprise-grade GRC automation platform with RAG capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnubhavPradhan/NexComply-analyser-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "sentence-transformers>=2.2.0",
        "openai>=1.0.0",
        "chromadb>=0.4.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "streamlit>=1.25.0",
        "plotly>=5.15.0",
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.11.0",
        "httpx>=0.24.0",
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-asyncio>=0.21.0",
        "tqdm>=4.65.0",
        "loguru>=0.7.0",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "reportlab>=4.0.0",
        "xlsxwriter>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
