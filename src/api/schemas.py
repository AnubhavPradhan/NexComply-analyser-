"""
API schemas for request and response models.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request model for compliance analysis."""
    framework: str = Field(..., description="Target compliance framework")
    policy_document: str = Field(..., description="Policy document text to analyze")
    top_k: int = Field(default=5, description="Number of top controls to retrieve")


class GapResult(BaseModel):
    """Model for a single compliance gap."""
    control_id: str
    framework: str
    requirement: str
    current_state: str
    severity: str
    confidence: float
    recommendations: List[str]


class AnalyzeResponse(BaseModel):
    """Response model for compliance analysis."""
    framework: str
    total_gaps: int
    gaps: List[Dict[str, Any]]
    summary: Dict[str, Any]


class RiskFactorRequest(BaseModel):
    """Request model for a risk factor."""
    name: str = Field(..., description="Name of the risk factor")
    category: str = Field(..., description="Risk category")
    likelihood: int = Field(..., ge=1, le=5, description="Likelihood score (1-5)")
    impact: int = Field(..., ge=1, le=5, description="Impact score (1-5)")
    current_controls: str = Field(..., description="Description of current controls")
    control_effectiveness: float = Field(..., ge=0, le=100, description="Control effectiveness (0-100)")


class AssessRiskRequest(BaseModel):
    """Request model for risk assessment."""
    risk_id: str = Field(..., description="Unique risk identifier")
    description: str = Field(..., description="Risk description")
    risk_factors: List[RiskFactorRequest] = Field(..., description="List of risk factors")


class AssessRiskResponse(BaseModel):
    """Response model for risk assessment."""
    risk_id: str
    description: str
    category: str
    inherent_risk_score: float
    residual_risk_score: float
    risk_level: str
    recommendations: List[str]
    assessment_date: str


class SearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str = Field(..., description="Search query")
    collection: str = Field(default="frameworks", description="Collection to search")
    top_k: int = Field(default=5, description="Number of results to return")
    filter_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filters")


class SearchResult(BaseModel):
    """Model for a search result."""
    document: str
    metadata: Dict[str, Any]
    distance: float
    id: str


class SearchResponse(BaseModel):
    """Response model for semantic search."""
    query: str
    results: List[Dict[str, Any]]
    total_results: int


class FrameworkInfo(BaseModel):
    """Model for framework information."""
    name: str
    description: str
    total_controls: int


class FrameworksResponse(BaseModel):
    """Response model for frameworks list."""
    frameworks: List[Dict[str, str]]
    total_frameworks: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str
    timestamp: str
