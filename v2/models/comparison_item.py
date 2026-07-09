"""
==========================================================
Comparison Item

Purpose
-------
Represents the comparison of a single business parameter
between two product specifications.

Each ComparisonItem represents one row in the final
comparison report.

==========================================================
"""

from dataclasses import dataclass


@dataclass
class ComparisonItem:

    # ======================================================
    # Parameter Information
    # ======================================================

    parameter_name: str = ""

    category: str = ""

    section: str = ""

    # ======================================================
    # Values
    # ======================================================

    old_value: str = ""

    new_value: str = ""

    # ======================================================
    # Comparison
    # ======================================================

    status: str = ""

    impact: str = ""

    reason: str = ""

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

    # ------------------------------------------------------

    def is_removed(self):

        return self.status == "Removed"

    # ------------------------------------------------------

    def is_modified(self):

        return self.status == "Modified"

    # ------------------------------------------------------

    def is_unchanged(self):

        return self.status == "Unchanged"

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "Parameter": self.parameter_name,

            "Category": self.category,

            "Section": self.section,

            "Old Value": self.old_value,

            "New Value": self.new_value,

            "Status": self.status,

            "Impact": self.impact,

            "Reason": self.reason,

            "Page V1": self.page_v1,

            "Page V2": self.page_v2,

            "Confidence V1": self.confidence_v1,

            "Confidence V2": self.confidence_v2

        }

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):

        return (
            f"{self.parameter_name} [{self.status}]"
        )