from dataclasses import dataclass, field
from typing import List


@dataclass
class BusinessAnalysis:
    """
    AI-generated business intelligence
    based on a BusinessChange object.
    """

    # -------------------------------
    # Executive Summary
    # -------------------------------

    summary: str = ""

    business_impact: str = ""

    # -------------------------------
    # Stakeholders
    # -------------------------------

    affected_teams: List[str] = field(default_factory=list)

    stakeholders: List[str] = field(default_factory=list)

    # -------------------------------
    # Testing
    # -------------------------------

    testing_recommendations: List[str] = field(default_factory=list)

    regression_required: bool = False

    uat_required: bool = False

    # -------------------------------
    # Business Governance
    # -------------------------------

    actuarial_review: bool = False

    compliance_review: bool = False

    legal_review: bool = False

    operations_review: bool = False

    migration_impact: bool = False

    customer_communication_required: bool = False

    business_criticality_score: int = 0

    # -------------------------------
    # Risk
    # -------------------------------

    risk: str = ""

    priority: str = ""

    business_criticality_score: int = 0

    # -------------------------------
    # AI Confidence
    # -------------------------------

    confidence: float = 0.0

    # -------------------------------
    # Future Expansion
    # -------------------------------

    recommendations: List[str] = field(default_factory=list)

    assumptions: List[str] = field(default_factory=list)

    notes: List[str] = field(default_factory=list)