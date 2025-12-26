"""
Unit tests for RAG Compliance Analyzer.
"""
import pytest
from unittest.mock import Mock, patch
import tempfile
from pathlib import Path

from src.models.compliance_analyzer import RAGComplianceAnalyzer


@pytest.fixture
def temp_db_path():
    """Create a temporary directory for the vector database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_controls():
    """Sample framework controls for testing."""
    return [
        {
            "control_id": "A.5.1.1",
            "title": "Policies for information security",
            "description": "A set of policies for information security shall be defined.",
            "category": "Information Security Policies",
            "criticality": "High",
            "status": "Not Implemented"
        },
        {
            "control_id": "A.8.2.1",
            "title": "Classification of information",
            "description": "Information shall be classified in terms of legal requirements.",
            "category": "Asset Management",
            "criticality": "High",
            "status": "Not Implemented"
        },
    ]


@pytest.fixture
def sample_policy():
    """Sample policy document for testing."""
    return """
    Information Security Policy
    
    This policy establishes the framework for information security management.
    All information assets must be classified according to their sensitivity.
    Access controls must be implemented for all systems.
    Regular security audits will be conducted.
    """


class TestRAGComplianceAnalyzer:
    """Test cases for RAGComplianceAnalyzer."""
    
    def test_initialization(self, temp_db_path):
        """Test analyzer initialization."""
        analyzer = RAGComplianceAnalyzer(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_db_path=temp_db_path
        )
        
        assert analyzer is not None
        assert analyzer.embedding_generator is not None
        assert analyzer.chroma_client is not None
    
    def test_index_framework(self, temp_db_path, sample_controls):
        """Test framework indexing."""
        analyzer = RAGComplianceAnalyzer(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_db_path=temp_db_path
        )
        
        # Index controls
        analyzer.index_framework("ISO27001", sample_controls)
        
        # Verify indexing by querying
        results = analyzer.semantic_search(
            query="information security policy",
            collection="frameworks",
            top_k=2,
            filter_metadata={"framework": "ISO27001"}
        )
        
        assert len(results) > 0
    
    def test_semantic_search(self, temp_db_path, sample_controls):
        """Test semantic search functionality."""
        analyzer = RAGComplianceAnalyzer(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_db_path=temp_db_path
        )
        
        # Index controls
        analyzer.index_framework("ISO27001", sample_controls)
        
        # Search
        results = analyzer.semantic_search(
            query="classification",
            collection="frameworks",
            top_k=1
        )
        
        assert len(results) > 0
        assert "metadata" in results[0]
        assert "document" in results[0]
    
    def test_chunk_document(self, temp_db_path, sample_policy):
        """Test document chunking."""
        analyzer = RAGComplianceAnalyzer(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_db_path=temp_db_path
        )
        
        chunks = analyzer._chunk_document(
            document=sample_policy,
            chunk_size=100,
            overlap=20
        )
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_analyze_compliance_gap(self, temp_db_path, sample_controls, sample_policy):
        """Test compliance gap analysis."""
        analyzer = RAGComplianceAnalyzer(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_db_path=temp_db_path
        )
        
        # Index framework
        analyzer.index_framework("ISO27001", sample_controls)
        
        # Analyze gaps
        gaps = analyzer.analyze_compliance_gap(
            framework="ISO27001",
            policy_document=sample_policy,
            top_k=2
        )
        
        assert isinstance(gaps, list)
        if len(gaps) > 0:
            gap = gaps[0]
            assert "control_id" in gap
            assert "severity" in gap
            assert "recommendations" in gap
    
    def test_deduplicate_gaps(self, temp_db_path):
        """Test gap deduplication."""
        analyzer = RAGComplianceAnalyzer(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
            vector_db_path=temp_db_path
        )
        
        gaps = [
            {"control_id": "A.5.1.1", "confidence": 0.7},
            {"control_id": "A.5.1.1", "confidence": 0.5},
            {"control_id": "A.8.2.1", "confidence": 0.6},
        ]
        
        unique_gaps = analyzer._deduplicate_gaps(gaps)
        
        assert len(unique_gaps) == 2
        # Should keep the gap with lower confidence (higher severity)
        a511_gap = next(g for g in unique_gaps if g["control_id"] == "A.5.1.1")
        assert a511_gap["confidence"] == 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
