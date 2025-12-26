"""
Application settings and configuration management.

This module provides centralized configuration management using Pydantic Settings,
supporting environment variables and default values.
"""
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    All settings can be overridden via environment variables.
    """
    
    # API Settings
    api_host: str = Field(default="0.0.0.0", description="API host address")
    api_port: int = Field(default=8000, description="API port number")
    api_version: str = Field(default="v1", description="API version")
    
    # Model Settings
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model name"
    )
    llm_model: str = Field(
        default="gpt-3.5-turbo",
        description="LLM model name"
    )
    
    # API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./nexcomply.db",
        description="Database connection URL"
    )
    vector_db_path: str = Field(
        default="./data/vector_db",
        description="Vector database storage path"
    )
    
    # Supported Frameworks
    supported_frameworks: List[str] = Field(
        default=[
            "ISO27001",
            "NIST-CSF",
            "SOC2",
            "GDPR",
            "HIPAA",
            "PCI-DSS",
            "CIS",
            "COBIT",
            "ITIL"
        ],
        description="List of supported compliance frameworks"
    )
    
    # Risk Configuration
    risk_levels: List[str] = Field(
        default=["Critical", "High", "Medium", "Low", "Minimal"],
        description="Risk level classifications"
    )
    
    risk_matrix_size: int = Field(
        default=5,
        description="Size of the risk matrix (5x5 by default)"
    )
    
    # Processing Settings
    workers: int = Field(
        default=4,
        description="Number of worker processes"
    )
    batch_size: int = Field(
        default=32,
        description="Batch size for processing"
    )
    chunk_size: int = Field(
        default=512,
        description="Document chunk size for processing"
    )
    chunk_overlap: int = Field(
        default=50,
        description="Overlap between document chunks"
    )
    
    # Application Settings
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode flag"
    )
    
    # CORS Settings
    cors_origins: List[str] = Field(
        default=["*"],
        description="Allowed CORS origins"
    )
    
    # Thresholds
    gap_severity_threshold: float = Field(
        default=0.7,
        description="Threshold for gap severity assessment"
    )
    confidence_threshold: float = Field(
        default=0.6,
        description="Minimum confidence score threshold"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the application settings instance.
    
    Returns:
        Settings: The global settings object.
    """
    return settings
