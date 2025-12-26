"""
Framework loader module.

Handles loading and parsing of compliance framework controls.
"""
from typing import List, Dict, Any, Optional
import json
import pandas as pd
from pathlib import Path
from loguru import logger


class FrameworkLoader:
    """
    Load and manage compliance framework controls.
    """
    
    def __init__(self, frameworks_path: str = "./Frameworks"):
        """
        Initialize the framework loader.
        
        Args:
            frameworks_path: Path to frameworks directory.
        """
        self.frameworks_path = Path(frameworks_path)
        self.frameworks_cache: Dict[str, List[Dict[str, Any]]] = {}
    
    def load_framework(self, framework_name: str) -> List[Dict[str, Any]]:
        """
        Load a compliance framework's controls.
        
        Args:
            framework_name: Name of the framework (e.g., 'ISO27001', 'NIST-CSF').
            
        Returns:
            List of control dictionaries.
        """
        # Check cache first
        if framework_name in self.frameworks_cache:
            logger.info(f"Loading {framework_name} from cache")
            return self.frameworks_cache[framework_name]
        
        logger.info(f"Loading framework: {framework_name}")
        
        # Try to load from Excel file
        excel_file = self.frameworks_path / "Frameworks for Security Posture_Review.xlsx"
        
        if excel_file.exists():
            controls = self._load_from_excel(excel_file, framework_name)
            self.frameworks_cache[framework_name] = controls
            return controls
        
        # If no file found, return default controls
        logger.warning(f"No framework file found for {framework_name}, using defaults")
        controls = self._get_default_controls(framework_name)
        self.frameworks_cache[framework_name] = controls
        return controls
    
    def _load_from_excel(
        self,
        file_path: Path,
        framework_name: str
    ) -> List[Dict[str, Any]]:
        """
        Load framework controls from Excel file.
        
        Args:
            file_path: Path to Excel file.
            framework_name: Name of the framework sheet.
            
        Returns:
            List of control dictionaries.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=framework_name)
            controls = []
            
            for _, row in df.iterrows():
                control = {
                    "control_id": str(row.get("Control ID", row.get("ID", ""))),
                    "title": str(row.get("Title", row.get("Control", ""))),
                    "description": str(row.get("Description", row.get("Requirement", ""))),
                    "category": str(row.get("Category", row.get("Domain", "General"))),
                    "criticality": str(row.get("Criticality", row.get("Priority", "Medium"))),
                    "status": str(row.get("Status", "Not Implemented")),
                }
                controls.append(control)
            
            logger.info(f"Loaded {len(controls)} controls for {framework_name}")
            return controls
            
        except Exception as e:
            logger.error(f"Error loading framework from Excel: {e}")
            return self._get_default_controls(framework_name)
    
    def _get_default_controls(self, framework_name: str) -> List[Dict[str, Any]]:
        """
        Get default controls for a framework.
        
        Args:
            framework_name: Name of the framework.
            
        Returns:
            List of default control dictionaries.
        """
        # Default controls based on framework
        default_controls = {
            "ISO27001": [
                {
                    "control_id": "A.5.1.1",
                    "title": "Policies for information security",
                    "description": "A set of policies for information security shall be defined, approved by management, published and communicated to employees and relevant external parties.",
                    "category": "Information Security Policies",
                    "criticality": "High",
                    "status": "Not Implemented"
                },
                {
                    "control_id": "A.8.2.1",
                    "title": "Classification of information",
                    "description": "Information shall be classified in terms of legal requirements, value, criticality and sensitivity to unauthorised disclosure or modification.",
                    "category": "Asset Management",
                    "criticality": "High",
                    "status": "Not Implemented"
                },
            ],
            "NIST-CSF": [
                {
                    "control_id": "ID.AM-1",
                    "title": "Physical devices and systems inventory",
                    "description": "Physical devices and systems within the organization are inventoried",
                    "category": "Identify",
                    "criticality": "High",
                    "status": "Not Implemented"
                },
                {
                    "control_id": "PR.AC-1",
                    "title": "Identity and credentials management",
                    "description": "Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes",
                    "category": "Protect",
                    "criticality": "High",
                    "status": "Not Implemented"
                },
            ],
            "SOC2": [
                {
                    "control_id": "CC6.1",
                    "title": "Logical and Physical Access Controls",
                    "description": "The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives.",
                    "category": "Common Criteria",
                    "criticality": "High",
                    "status": "Not Implemented"
                },
            ],
        }
        
        return default_controls.get(framework_name, [
            {
                "control_id": "CTRL-001",
                "title": "Default Control",
                "description": "Default control for framework",
                "category": "General",
                "criticality": "Medium",
                "status": "Not Implemented"
            }
        ])
    
    def get_available_frameworks(self) -> List[str]:
        """
        Get list of available frameworks.
        
        Returns:
            List of framework names.
        """
        return [
            "ISO27001",
            "NIST-CSF",
            "SOC2",
            "GDPR",
            "HIPAA",
            "PCI-DSS",
            "CIS",
            "COBIT",
            "ITIL"
        ]
