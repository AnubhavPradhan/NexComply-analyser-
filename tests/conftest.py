"""Shared test fixtures and configuration."""

import pytest


@pytest.fixture
def sample_policy_text():
    """Provide sample policy document text."""
    return """
    Information Security Policy

    1. Purpose
    This policy establishes the requirements for information security.

    2. Scope
    This policy applies to all employees and contractors.

    3. Controls
    - Access control
    - Data encryption
    - Incident response
    """


@pytest.fixture
def sample_questionnaire_data():
    """Provide sample questionnaire data."""
    return {
        "questions": [
            {
                "id": "Q1",
                "text": "Do you have an information security policy?",
                "category": "governance",
                "answer": "yes",
            },
            {
                "id": "Q2",
                "text": "Are security assessments performed annually?",
                "category": "risk_management",
                "answer": "partial",
            },
        ]
    }
