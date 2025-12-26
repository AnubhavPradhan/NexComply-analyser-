"""
Reporting utility module.

Provides functions for generating compliance and risk reports in various formats.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from io import BytesIO
from loguru import logger


class ReportGenerator:
    """
    Generate compliance and risk reports in various formats.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        pass
    
    def generate_compliance_report(
        self,
        gaps: List[Dict[str, Any]],
        framework: str,
        organization: str = "Organization"
    ) -> pd.DataFrame:
        """
        Generate a compliance gap report as a DataFrame.
        
        Args:
            gaps: List of compliance gaps.
            framework: Target compliance framework.
            organization: Organization name.
            
        Returns:
            pd.DataFrame: Report data.
        """
        logger.info(f"Generating compliance report for {framework}")
        
        report_data = []
        for gap in gaps:
            report_data.append({
                "Control ID": gap.get("control_id", "N/A"),
                "Framework": framework,
                "Requirement": gap.get("requirement", ""),
                "Current State": gap.get("current_state", ""),
                "Gap Severity": gap.get("severity", ""),
                "Confidence": f"{gap.get('confidence', 0):.2%}",
                "Recommendations": "; ".join(gap.get("recommendations", [])),
            })
        
        df = pd.DataFrame(report_data)
        return df
    
    def generate_risk_report(
        self,
        risk_assessments: List[Dict[str, Any]],
        organization: str = "Organization"
    ) -> pd.DataFrame:
        """
        Generate a risk assessment report as a DataFrame.
        
        Args:
            risk_assessments: List of risk assessments.
            organization: Organization name.
            
        Returns:
            pd.DataFrame: Report data.
        """
        logger.info("Generating risk assessment report")
        
        report_data = []
        for assessment in risk_assessments:
            report_data.append({
                "Risk ID": assessment.get("risk_id", "N/A"),
                "Description": assessment.get("description", ""),
                "Category": assessment.get("category", ""),
                "Inherent Risk": assessment.get("inherent_risk_score", 0),
                "Residual Risk": assessment.get("residual_risk_score", 0),
                "Risk Level": assessment.get("risk_level", ""),
                "Recommendations": "; ".join(assessment.get("recommendations", [])),
            })
        
        df = pd.DataFrame(report_data)
        return df
    
    def export_to_csv(self, df: pd.DataFrame) -> bytes:
        """
        Export DataFrame to CSV format.
        
        Args:
            df: DataFrame to export.
            
        Returns:
            bytes: CSV file content.
        """
        logger.info("Exporting report to CSV")
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()
    
    def export_to_excel(self, df: pd.DataFrame, sheet_name: str = "Report") -> bytes:
        """
        Export DataFrame to Excel format.
        
        Args:
            df: DataFrame to export.
            sheet_name: Name of the Excel sheet.
            
        Returns:
            bytes: Excel file content.
        """
        logger.info("Exporting report to Excel")
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        return buffer.getvalue()
    
    def generate_summary_stats(self, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for compliance gaps.
        
        Args:
            gaps: List of compliance gaps.
            
        Returns:
            Dict containing summary statistics.
        """
        if not gaps:
            return {
                "total_gaps": 0,
                "critical_gaps": 0,
                "high_gaps": 0,
                "medium_gaps": 0,
                "low_gaps": 0,
            }
        
        severity_counts = {}
        for gap in gaps:
            severity = gap.get("severity", "Unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "total_gaps": len(gaps),
            "critical_gaps": severity_counts.get("Critical", 0),
            "high_gaps": severity_counts.get("High", 0),
            "medium_gaps": severity_counts.get("Medium", 0),
            "low_gaps": severity_counts.get("Low", 0),
            "severity_distribution": severity_counts,
        }
