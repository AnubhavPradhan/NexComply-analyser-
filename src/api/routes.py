"""
FastAPI routes for NexComply Analyzer API.
"""
from typing import List, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.config.settings import get_settings, Settings
from src.api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    AssessRiskRequest,
    AssessRiskResponse,
    SearchRequest,
    SearchResponse,
    FrameworksResponse,
    HealthResponse,
)
from src.models.compliance_analyzer import RAGComplianceAnalyzer
from src.models.risk_assessor import AdvancedRiskAssessor, RiskFactor
from src.data.framework_loader import FrameworkLoader
from src.utils.reporting import ReportGenerator

# Global instances (lazy initialization)
_analyzer: RAGComplianceAnalyzer = None
_risk_assessor: AdvancedRiskAssessor = None
_framework_loader: FrameworkLoader = None
_report_generator: ReportGenerator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting NexComply Analyzer API")
    logger.info(f"API Version: 1.0.0")
    settings = get_settings()
    logger.info(f"Embedding Model: {settings.embedding_model}")
    logger.info(f"Vector DB Path: {settings.vector_db_path}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down NexComply Analyzer API")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="NexComply Analyzer API",
    description="Enterprise-grade GRC automation platform with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_analyzer() -> RAGComplianceAnalyzer:
    """Get or create compliance analyzer instance."""
    global _analyzer
    if _analyzer is None:
        logger.info("Initializing RAG Compliance Analyzer")
        _analyzer = RAGComplianceAnalyzer(
            embedding_model_name=settings.embedding_model,
            vector_db_path=settings.vector_db_path,
        )
    return _analyzer


def get_risk_assessor() -> AdvancedRiskAssessor:
    """Get or create risk assessor instance."""
    global _risk_assessor
    if _risk_assessor is None:
        logger.info("Initializing Advanced Risk Assessor")
        _risk_assessor = AdvancedRiskAssessor()
    return _risk_assessor


def get_framework_loader() -> FrameworkLoader:
    """Get or create framework loader instance."""
    global _framework_loader
    if _framework_loader is None:
        logger.info("Initializing Framework Loader")
        _framework_loader = FrameworkLoader()
    return _framework_loader


def get_report_generator() -> ReportGenerator:
    """Get or create report generator instance."""
    global _report_generator
    if _report_generator is None:
        logger.info("Initializing Report Generator")
        _report_generator = ReportGenerator()
    return _report_generator


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: API health status.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze_compliance(
    request: AnalyzeRequest,
    analyzer: RAGComplianceAnalyzer = Depends(get_analyzer),
    framework_loader: FrameworkLoader = Depends(get_framework_loader),
    report_generator: ReportGenerator = Depends(get_report_generator),
):
    """
    Analyze compliance gaps between policy and framework.
    
    Args:
        request: Analysis request containing framework and policy document.
        
    Returns:
        AnalyzeResponse: Compliance analysis results with gaps and recommendations.
    """
    try:
        logger.info(f"Analyzing compliance for framework: {request.framework}")
        
        # Validate framework
        if request.framework not in framework_loader.get_available_frameworks():
            raise HTTPException(
                status_code=400,
                detail=f"Framework '{request.framework}' not supported"
            )
        
        # Load and index framework if not already done
        controls = framework_loader.load_framework(request.framework)
        analyzer.index_framework(request.framework, controls)
        
        # Perform gap analysis
        gaps = analyzer.analyze_compliance_gap(
            framework=request.framework,
            policy_document=request.policy_document,
            top_k=request.top_k
        )
        
        # Generate summary statistics
        summary = report_generator.generate_summary_stats(gaps)
        
        return AnalyzeResponse(
            framework=request.framework,
            total_gaps=len(gaps),
            gaps=gaps,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error in compliance analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/assess-risk", response_model=AssessRiskResponse)
async def assess_risk(
    request: AssessRiskRequest,
    risk_assessor: AdvancedRiskAssessor = Depends(get_risk_assessor),
):
    """
    Perform risk assessment with multi-factor analysis.
    
    Args:
        request: Risk assessment request containing risk factors.
        
    Returns:
        AssessRiskResponse: Risk assessment results with recommendations.
    """
    try:
        logger.info(f"Assessing risk: {request.risk_id}")
        
        # Convert request risk factors to RiskFactor objects
        risk_factors = [
            RiskFactor(
                name=rf.name,
                category=rf.category,
                likelihood=rf.likelihood,
                impact=rf.impact,
                current_controls=rf.current_controls,
                control_effectiveness=rf.control_effectiveness
            )
            for rf in request.risk_factors
        ]
        
        # Perform risk assessment
        assessment = risk_assessor.assess_risk(
            risk_factors=risk_factors,
            risk_id=request.risk_id,
            description=request.description
        )
        
        return AssessRiskResponse(
            risk_id=assessment.risk_id,
            description=assessment.description,
            category=assessment.category,
            inherent_risk_score=assessment.inherent_risk_score,
            residual_risk_score=assessment.residual_risk_score,
            risk_level=assessment.risk_level,
            recommendations=assessment.recommendations,
            assessment_date=assessment.assessment_date
        )
        
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/search", response_model=SearchResponse)
async def semantic_search(
    request: SearchRequest,
    analyzer: RAGComplianceAnalyzer = Depends(get_analyzer),
):
    """
    Perform semantic search across frameworks or policies.
    
    Args:
        request: Search request containing query and parameters.
        
    Returns:
        SearchResponse: Search results with relevant documents.
    """
    try:
        logger.info(f"Performing semantic search: {request.query}")
        
        # Validate collection
        if request.collection not in ["frameworks", "policies"]:
            raise HTTPException(
                status_code=400,
                detail="Collection must be 'frameworks' or 'policies'"
            )
        
        # Perform search
        results = analyzer.semantic_search(
            query=request.query,
            collection=request.collection,
            top_k=request.top_k,
            filter_metadata=request.filter_metadata
        )
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results)
        )
        
    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/frameworks", response_model=FrameworksResponse)
async def list_frameworks(
    framework_loader: FrameworkLoader = Depends(get_framework_loader),
):
    """
    List all available compliance frameworks.
    
    Returns:
        FrameworksResponse: List of supported frameworks.
    """
    try:
        frameworks = framework_loader.get_available_frameworks()
        
        framework_info = [
            {
                "name": fw,
                "description": f"{fw} compliance framework",
                "status": "available"
            }
            for fw in frameworks
        ]
        
        return FrameworksResponse(
            frameworks=framework_info,
            total_frameworks=len(frameworks)
        )
        
    except Exception as e:
        logger.error(f"Error listing frameworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.routes:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
