"""Ingestion module for loading policy docs, questionnaires, and frameworks."""

from pathlib import Path
from typing import Dict, List, Optional

from .parsing import parse_document_metadata
from .utils import get_data_dir, get_logger, list_files

logger = get_logger(__name__)


class DataIngestion:
    """Handle ingestion of various data sources."""
    
    def __init__(self):
        """Initialize the data ingestion handler."""
        self.data_sources = {
            "policy_docs": "New Format Policy Docs",
            "questionnaires": "Questionnaires",
            "frameworks": "Frameworks",
            "risk_reports": "Risk Reports",
            "dummy_kl": "Dummy KL",
            "session_grc": "Session on GRC",
        }
    
    def ingest_policy_documents(self) -> List[Dict[str, str]]:
        """Ingest policy documents.
        
        Returns:
            List of document metadata dictionaries
        """
        policy_dir = get_data_dir(self.data_sources["policy_docs"])
        logger.info(f"Ingesting policy documents from: {policy_dir}")
        
        files = list_files(policy_dir, extensions=['.pdf', '.docx', '.doc'])
        documents = []
        
        for filepath in files:
            metadata = parse_document_metadata(filepath)
            documents.append(metadata)
            logger.debug(f"Found policy document: {metadata['name']}")
        
        logger.info(f"Ingested {len(documents)} policy documents")
        return documents
    
    def ingest_questionnaires(self) -> List[Dict[str, str]]:
        """Ingest questionnaires.
        
        Returns:
            List of questionnaire metadata dictionaries
        """
        questionnaire_dir = get_data_dir(self.data_sources["questionnaires"])
        logger.info(f"Ingesting questionnaires from: {questionnaire_dir}")
        
        files = list_files(questionnaire_dir, extensions=['.xlsx', '.xls'])
        questionnaires = []
        
        for filepath in files:
            metadata = parse_document_metadata(filepath)
            questionnaires.append(metadata)
            logger.debug(f"Found questionnaire: {metadata['name']}")
        
        logger.info(f"Ingested {len(questionnaires)} questionnaires")
        return questionnaires
    
    def ingest_frameworks(self) -> List[Dict[str, str]]:
        """Ingest framework documents.
        
        Returns:
            List of framework metadata dictionaries
        """
        framework_dir = get_data_dir(self.data_sources["frameworks"])
        logger.info(f"Ingesting frameworks from: {framework_dir}")
        
        files = list_files(framework_dir, extensions=['.xlsx', '.xls', '.pdf'])
        frameworks = []
        
        for filepath in files:
            metadata = parse_document_metadata(filepath)
            frameworks.append(metadata)
            logger.debug(f"Found framework: {metadata['name']}")
        
        logger.info(f"Ingested {len(frameworks)} frameworks")
        return frameworks
    
    def ingest_all(self) -> Dict[str, List[Dict[str, str]]]:
        """Ingest all data sources.
        
        Returns:
            Dictionary with all ingested data
        """
        logger.info("Starting full data ingestion")
        
        data = {
            "policy_documents": self.ingest_policy_documents(),
            "questionnaires": self.ingest_questionnaires(),
            "frameworks": self.ingest_frameworks(),
        }
        
        total_items = sum(len(items) for items in data.values())
        logger.info(f"Ingestion complete. Total items: {total_items}")
        
        return data
