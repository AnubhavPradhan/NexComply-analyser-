"""Framework mapping structures and loaders."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from .utils import get_data_dir, get_logger, list_files

logger = get_logger(__name__)


class FrameworkType(Enum):
    """Types of compliance frameworks."""

    ISO27001 = "iso27001"
    SOC2 = "soc2"
    NIST = "nist"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    CUSTOM = "custom"


@dataclass
class FrameworkControl:
    """Represents a single framework control."""

    control_id: str
    control_name: str
    description: str
    framework: FrameworkType
    category: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "control_id": self.control_id,
            "control_name": self.control_name,
            "description": self.description,
            "framework": self.framework.value,
            "category": self.category or "general",
        }


@dataclass
class Framework:
    """Represents a compliance framework."""

    name: str
    framework_type: FrameworkType
    controls: List[FrameworkControl]
    version: Optional[str] = None

    def get_control_count(self) -> int:
        """Get total number of controls.

        Returns:
            Number of controls
        """
        return len(self.controls)

    def get_controls_by_category(self) -> Dict[str, List[FrameworkControl]]:
        """Group controls by category.

        Returns:
            Dictionary mapping categories to controls
        """
        categorized: Dict[str, List[FrameworkControl]] = {}

        for control in self.controls:
            category = control.category or "general"
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(control)

        return categorized


class FrameworkLoader:
    """Load framework data from files."""

    def __init__(self):
        """Initialize the framework loader."""
        self.frameworks_dir = get_data_dir("Frameworks")

    def list_framework_files(self) -> List[Path]:
        """List available framework files.

        Returns:
            List of framework file paths
        """
        return list_files(self.frameworks_dir, extensions=[".xlsx", ".xls", ".pdf"])

    def load_sample_framework(self) -> Framework:
        """Load a sample framework for demonstration.

        Returns:
            Sample framework instance
        """
        logger.info("Loading sample framework")

        sample_controls = [
            FrameworkControl(
                control_id="A.5.1",
                control_name="Information Security Policy",
                description="Policies for information security shall be defined",
                framework=FrameworkType.ISO27001,
                category="governance",
            ),
            FrameworkControl(
                control_id="A.8.1",
                control_name="Asset Management",
                description="Assets associated with information shall be identified",
                framework=FrameworkType.ISO27001,
                category="asset_management",
            ),
            FrameworkControl(
                control_id="A.9.1",
                control_name="Access Control",
                description="Access to information and systems shall be controlled",
                framework=FrameworkType.ISO27001,
                category="access_control",
            ),
        ]

        return Framework(
            name="ISO 27001 Sample",
            framework_type=FrameworkType.ISO27001,
            controls=sample_controls,
            version="2022",
        )

    def get_framework_summary(self) -> Dict[str, int]:
        """Get summary of available frameworks.

        Returns:
            Dictionary with framework counts
        """
        files = self.list_framework_files()
        return {
            "total_files": len(files),
            "xlsx_files": len([f for f in files if f.suffix in [".xlsx", ".xls"]]),
            "pdf_files": len([f for f in files if f.suffix == ".pdf"]),
        }
