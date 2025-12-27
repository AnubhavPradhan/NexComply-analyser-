"""Questionnaire structures and scoring logic."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from .utils import get_logger

logger = get_logger(__name__)


class QuestionnaireCategory(Enum):
    """Categories for questionnaire items."""

    GOVERNANCE = "governance"
    RISK_MANAGEMENT = "risk_management"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    DATA_PRIVACY = "data_privacy"
    OPERATIONS = "operations"
    GENERAL = "general"


class RiskLevel(Enum):
    """Risk levels for assessment."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class QuestionnaireItem:
    """Represents a single questionnaire item."""

    question_id: str
    question_text: str
    category: QuestionnaireCategory = QuestionnaireCategory.GENERAL
    answer: Optional[str] = None
    risk_level: Optional[RiskLevel] = None

    def score(self) -> int:
        """Calculate a simple score for the item.

        Returns:
            Score value (0-100)
        """
        if self.answer is None:
            return 0

        # Simple scoring logic
        answer_lower = self.answer.lower()

        if any(word in answer_lower for word in ["yes", "implemented", "compliant"]):
            return 80
        elif any(word in answer_lower for word in ["partial", "in progress"]):
            return 50
        elif any(word in answer_lower for word in ["no", "not implemented"]):
            return 20
        else:
            return 40


@dataclass
class Questionnaire:
    """Represents a complete questionnaire."""

    name: str
    items: List[QuestionnaireItem]
    metadata: Optional[Dict[str, str]] = None

    def calculate_overall_score(self) -> float:
        """Calculate overall questionnaire score.

        Returns:
            Overall score (0-100)
        """
        if not self.items:
            return 0.0

        total_score = sum(item.score() for item in self.items)
        return total_score / len(self.items)

    def get_category_scores(self) -> Dict[str, float]:
        """Get scores by category.

        Returns:
            Dictionary mapping categories to scores
        """
        category_items: Dict[QuestionnaireCategory, List[QuestionnaireItem]] = {}

        for item in self.items:
            if item.category not in category_items:
                category_items[item.category] = []
            category_items[item.category].append(item)

        category_scores = {}
        for category, items in category_items.items():
            total_score = sum(item.score() for item in items)
            avg_score = total_score / len(items) if items else 0.0
            category_scores[category.value] = avg_score

        return category_scores

    def get_risk_summary(self) -> Dict[str, int]:
        """Get summary of risk levels.

        Returns:
            Dictionary with counts per risk level
        """
        risk_counts = {level.name: 0 for level in RiskLevel}

        for item in self.items:
            if item.risk_level:
                risk_counts[item.risk_level.name] += 1

        return risk_counts
