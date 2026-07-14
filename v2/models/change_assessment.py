"""
==========================================================
Change Assessment

Purpose
-------
Represents the AI-generated business assessment for a
single product parameter change.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class ChangeAssessment:

    # ======================================================
    # Difference Summary (AI Generated)
    # ======================================================

    difference_summary: str = ""

    # ======================================================
    # Business Assessment
    # ======================================================

    business_impact: str = ""

    executive_summary: str = ""

    remarks: str = ""

    # ======================================================
    # Risk Assessment
    # ======================================================

    risk: str = ""

    priority: str = ""

    business_criticality: str = ""

    # ======================================================
    # Implementation
    # ======================================================

    testing_recommendation: str = ""

    affected_teams: list[str] = field(default_factory=list)

    # ======================================================
    # Helper
    # ======================================================

    def affected_teams_text(self):

        return ", ".join(self.affected_teams)

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "difference_summary": self.difference_summary,

            "business_impact": self.business_impact,

            "executive_summary": self.executive_summary,

            "remarks": self.remarks,

            "risk": self.risk,

            "priority": self.priority,

            "business_criticality": self.business_criticality,

            "testing_recommendation": self.testing_recommendation,

            "affected_teams": self.affected_teams

        }

    # ======================================================
    # Pretty Print
    # ======================================================

    def print_summary(self):

        print()

        print("=" * 80)

        print("CHANGE ASSESSMENT")

        print("=" * 80)

        print(f"Risk                 : {self.risk}")

        print(f"Priority             : {self.priority}")

        print(f"Business Criticality : {self.business_criticality}")

        print(f"Affected Teams       : {self.affected_teams_text()}")

        print()

        print("Difference Summary")

        print("------------------------------")

        print(self.difference_summary)

        print()

        print("Business Impact")

        print("------------------------------")

        print(self.business_impact)

        print()

        print("Testing Recommendation")

        print("------------------------------")

        print(self.testing_recommendation)

        print()

        print("Remarks")

        print("------------------------------")

        print(self.remarks)

        print()

        print("=" * 80)