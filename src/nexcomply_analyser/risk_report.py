"""Risk report generation module."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict

from .frameworks import FrameworkLoader
from .ingestion import DataIngestion
from .questionnaire import Questionnaire, QuestionnaireCategory, QuestionnaireItem
from .utils import ensure_dir, get_data_dir, get_logger

logger = get_logger(__name__)


class RiskReportGenerator:
    """Generate risk reports from ingested data."""

    def __init__(self):
        """Initialize the risk report generator."""
        self.output_dir = get_data_dir("Risk Reports")
        self.ingestion = DataIngestion()
        self.framework_loader = FrameworkLoader()

    def generate_dummy_risk_score(self, category: str) -> float:
        """Generate a dummy risk score for a category.

        Args:
            category: Category name

        Returns:
            Risk score (0-100)
        """
        # Simple hash-based scoring for consistency
        score = (hash(category) % 50) + 25  # Range: 25-75
        return float(score)

    def collect_data(self) -> Dict[str, any]:
        """Collect all data for report generation.

        Returns:
            Dictionary with collected data
        """
        logger.info("Collecting data for risk report")

        # Ingest data
        ingested_data = self.ingestion.ingest_all()

        # Get framework info
        framework_summary = self.framework_loader.get_framework_summary()

        # Create sample questionnaire
        sample_items = [
            QuestionnaireItem(
                question_id="Q1",
                question_text="Is there a documented information security policy?",
                category=QuestionnaireCategory.GOVERNANCE,
                answer="yes",
            ),
            QuestionnaireItem(
                question_id="Q2",
                question_text="Are security assessments conducted regularly?",
                category=QuestionnaireCategory.SECURITY,
                answer="partial",
            ),
            QuestionnaireItem(
                question_id="Q3",
                question_text="Is data encrypted at rest and in transit?",
                category=QuestionnaireCategory.DATA_PRIVACY,
                answer="yes",
            ),
        ]

        questionnaire = Questionnaire(name="Sample Risk Assessment", items=sample_items)

        return {
            "ingested_data": ingested_data,
            "framework_summary": framework_summary,
            "questionnaire": questionnaire,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_csv_report(self, data: Dict[str, any], filename: str = "risk_report.csv") -> Path:
        """Generate a CSV risk report.

        Args:
            data: Collected data
            filename: Output filename

        Returns:
            Path to the generated CSV file
        """
        ensure_dir(self.output_dir)
        output_path = self.output_dir / filename

        logger.info(f"Generating CSV report: {output_path}")

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Header
            writer.writerow(["Category", "Count", "Risk Score", "Status"])

            # Policy documents
            policy_count = len(data["ingested_data"]["policy_documents"])
            writer.writerow(
                [
                    "Policy Documents",
                    policy_count,
                    self.generate_dummy_risk_score("policy"),
                    "Reviewed",
                ]
            )

            # Questionnaires
            questionnaire_count = len(data["ingested_data"]["questionnaires"])
            writer.writerow(
                [
                    "Questionnaires",
                    questionnaire_count,
                    self.generate_dummy_risk_score("questionnaire"),
                    "In Progress",
                ]
            )

            # Frameworks
            framework_count = len(data["ingested_data"]["frameworks"])
            writer.writerow(
                [
                    "Frameworks",
                    framework_count,
                    self.generate_dummy_risk_score("framework"),
                    "Active",
                ]
            )

            # Questionnaire categories
            if data.get("questionnaire"):
                category_scores = data["questionnaire"].get_category_scores()
                for category, score in category_scores.items():
                    writer.writerow(
                        [
                            f"Questionnaire - {category}",
                            len(
                                [
                                    i
                                    for i in data["questionnaire"].items
                                    if i.category.value == category
                                ]
                            ),
                            score,
                            "Assessed",
                        ]
                    )

        logger.info(f"CSV report generated successfully: {output_path}")
        return output_path

    def generate_json_report(
        self, data: Dict[str, any], filename: str = "risk_report.json"
    ) -> Path:
        """Generate a JSON risk report.

        Args:
            data: Collected data
            filename: Output filename

        Returns:
            Path to the generated JSON file
        """
        ensure_dir(self.output_dir)
        output_path = self.output_dir / filename

        logger.info(f"Generating JSON report: {output_path}")

        report = {
            "report_metadata": {
                "generated_at": data["timestamp"],
                "version": "0.1.0",
                "report_type": "risk_assessment",
            },
            "summary": {
                "policy_documents": len(data["ingested_data"]["policy_documents"]),
                "questionnaires": len(data["ingested_data"]["questionnaires"]),
                "frameworks": len(data["ingested_data"]["frameworks"]),
            },
            "risk_scores": {
                "policy_documents": self.generate_dummy_risk_score("policy"),
                "questionnaires": self.generate_dummy_risk_score("questionnaire"),
                "frameworks": self.generate_dummy_risk_score("framework"),
            },
            "framework_summary": data["framework_summary"],
        }

        if data.get("questionnaire"):
            report["questionnaire_analysis"] = {
                "overall_score": data["questionnaire"].calculate_overall_score(),
                "category_scores": data["questionnaire"].get_category_scores(),
                "risk_summary": data["questionnaire"].get_risk_summary(),
            }

        with open(output_path, "w", encoding="utf-8") as jsonfile:
            json.dump(report, jsonfile, indent=2)

        logger.info(f"JSON report generated successfully: {output_path}")
        return output_path

    def generate_reports(self) -> Dict[str, Path]:
        """Generate all risk reports.

        Returns:
            Dictionary with paths to generated reports
        """
        logger.info("Starting risk report generation")

        # Collect data
        data = self.collect_data()

        # Generate reports
        timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = self.generate_csv_report(data, f"risk_report_{timestamp_suffix}.csv")
        json_path = self.generate_json_report(data, f"risk_report_{timestamp_suffix}.json")

        logger.info("Risk report generation complete")

        return {
            "csv": csv_path,
            "json": json_path,
        }
