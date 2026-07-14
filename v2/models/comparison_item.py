"""
==========================================================
Comparison Item

Purpose
-------
Represents one compared business parameter.

One ComparisonItem = One row in the final report.

==========================================================
"""

from dataclasses import dataclass

from v2.models.difference_result import DifferenceResult


@dataclass
class ComparisonItem:

    # ======================================================
    # Parameter Information
    # ======================================================

    parameter_name: str = ""

    matched_parameter: str = ""

    category: str = ""

    section: str = ""

    # ======================================================
    # Values
    # ======================================================

    old_value: str = ""

    new_value: str = ""

    # Structured Difference Object
    difference_result: DifferenceResult | None = None

    # Human-readable Difference
    difference_summary: str = ""

    # ======================================================
    # Comparison
    # ======================================================

    status: str = ""

    impact: str = ""

    reason: str = ""

    # ======================================================
    # Confidence
    # ======================================================

    parameter_confidence: float = 0.0

    description_confidence: float = 0.0

    overall_confidence: float = 0.0

    confidence_band: str = ""

    # ======================================================
    # Classification
    # ======================================================

    decision: str = ""

    change_type: str = ""

    severity: str = ""

    # ======================================================
    # AI Assessment
    # ======================================================

    summary: str = ""

    business_impact: str = ""

    affected_teams: str = ""

    testing_recommendation: str = ""

    risk: str = ""

    priority: str = ""

    business_criticality: str = ""

    remarks: str = ""

    # Optional alias (keeps compatibility with older code)
    executive_summary: str = ""

    # ======================================================
    # Traceability
    # ======================================================

    page_v1: int = 0

    page_v2: int = 0

    confidence_v1: float = 0.0

    confidence_v2: float = 0.0

    # ======================================================
    # Helper Methods
    # ======================================================

    def is_added(self):
        return self.status == "Added"

    def is_removed(self):
        return self.status == "Removed"

    def is_modified(self):
        return self.status == "Modified"

    def is_unchanged(self):
        return self.status == "Unchanged"

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "Parameter": self.parameter_name,
            "Matched Parameter": self.matched_parameter,
            "Category": self.category,
            "Section": self.section,
            "Old Value": self.old_value,
            "New Value": self.new_value,
            "Difference": self.difference_summary,
            "Status": self.status,
            "Impact": self.impact,
            "Reason": self.reason,
            "Parameter Confidence": self.parameter_confidence,
            "Description Confidence": self.description_confidence,
            "Overall Confidence": self.overall_confidence,
            "Decision": self.decision,
            "Change Type": self.change_type,
            "Severity": self.severity,
            "Summary": self.summary,
            "Business Impact": self.business_impact,
            "Affected Teams": self.affected_teams,
            "Testing Recommendation": self.testing_recommendation,
            "Risk": self.risk,
            "Priority": self.priority,
            "Business Criticality": self.business_criticality,
            "Remarks": self.remarks,
            "Page V1": self.page_v1,
            "Page V2": self.page_v2

        }

    def __str__(self):

        return f"{self.parameter_name} [{self.status}]"