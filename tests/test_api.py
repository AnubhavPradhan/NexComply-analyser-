"""
API endpoint tests.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.api.routes import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestFrameworksEndpoint:
    """Test frameworks listing endpoint."""
    
    @patch('src.api.routes.get_framework_loader')
    def test_list_frameworks(self, mock_loader, client):
        """Test frameworks listing."""
        # Mock framework loader
        mock_instance = Mock()
        mock_instance.get_available_frameworks.return_value = [
            "ISO27001", "NIST-CSF", "SOC2"
        ]
        mock_loader.return_value = mock_instance
        
        response = client.get("/api/v1/frameworks")
        
        assert response.status_code == 200
        data = response.json()
        assert "frameworks" in data
        assert data["total_frameworks"] == 3


class TestAnalyzeEndpoint:
    """Test compliance analysis endpoint."""
    
    @patch('src.api.routes.get_analyzer')
    @patch('src.api.routes.get_framework_loader')
    @patch('src.api.routes.get_report_generator')
    def test_analyze_compliance(
        self,
        mock_report_gen,
        mock_loader,
        mock_analyzer,
        client
    ):
        """Test compliance analysis endpoint."""
        # Mock dependencies
        mock_loader_instance = Mock()
        mock_loader_instance.get_available_frameworks.return_value = ["ISO27001"]
        mock_loader_instance.load_framework.return_value = []
        mock_loader.return_value = mock_loader_instance
        
        mock_analyzer_instance = Mock()
        mock_analyzer_instance.analyze_compliance_gap.return_value = [
            {
                "control_id": "A.5.1.1",
                "framework": "ISO27001",
                "requirement": "Test requirement",
                "current_state": "Test state",
                "severity": "High",
                "confidence": 0.8,
                "recommendations": ["Test recommendation"]
            }
        ]
        mock_analyzer.return_value = mock_analyzer_instance
        
        mock_report_instance = Mock()
        mock_report_instance.generate_summary_stats.return_value = {
            "total_gaps": 1,
            "critical_gaps": 0,
            "high_gaps": 1
        }
        mock_report_gen.return_value = mock_report_instance
        
        # Make request
        response = client.post(
            "/api/v1/analyze",
            json={
                "framework": "ISO27001",
                "policy_document": "Test policy document",
                "top_k": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "framework" in data
        assert "total_gaps" in data
        assert "gaps" in data
    
    def test_analyze_invalid_framework(self, client):
        """Test analysis with invalid framework."""
        response = client.post(
            "/api/v1/analyze",
            json={
                "framework": "INVALID_FRAMEWORK",
                "policy_document": "Test policy",
                "top_k": 5
            }
        )
        
        # Should return error for invalid framework
        assert response.status_code in [400, 500]


class TestRiskAssessmentEndpoint:
    """Test risk assessment endpoint."""
    
    @patch('src.api.routes.get_risk_assessor')
    def test_assess_risk(self, mock_assessor, client):
        """Test risk assessment endpoint."""
        # Mock risk assessor
        mock_instance = Mock()
        mock_assessment = Mock()
        mock_assessment.risk_id = "RISK-001"
        mock_assessment.description = "Test risk"
        mock_assessment.category = "Technical"
        mock_assessment.inherent_risk_score = 15.0
        mock_assessment.residual_risk_score = 8.0
        mock_assessment.risk_level = "Medium"
        mock_assessment.recommendations = ["Test recommendation"]
        mock_assessment.assessment_date = "2024-01-01T00:00:00"
        
        mock_instance.assess_risk.return_value = mock_assessment
        mock_assessor.return_value = mock_instance
        
        # Make request
        response = client.post(
            "/api/v1/assess-risk",
            json={
                "risk_id": "RISK-001",
                "description": "Test risk description",
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
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["risk_id"] == "RISK-001"
        assert "risk_level" in data


class TestSearchEndpoint:
    """Test semantic search endpoint."""
    
    @patch('src.api.routes.get_analyzer')
    def test_semantic_search(self, mock_analyzer, client):
        """Test semantic search endpoint."""
        # Mock analyzer
        mock_instance = Mock()
        mock_instance.semantic_search.return_value = [
            {
                "document": "Test document",
                "metadata": {"test": "metadata"},
                "distance": 0.5,
                "id": "test_id"
            }
        ]
        mock_analyzer.return_value = mock_instance
        
        # Make request
        response = client.post(
            "/api/v1/search",
            json={
                "query": "test query",
                "collection": "frameworks",
                "top_k": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert data["total_results"] == 1
    
    def test_search_invalid_collection(self, client):
        """Test search with invalid collection."""
        response = client.post(
            "/api/v1/search",
            json={
                "query": "test query",
                "collection": "invalid_collection",
                "top_k": 5
            }
        )
        
        assert response.status_code in [400, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
