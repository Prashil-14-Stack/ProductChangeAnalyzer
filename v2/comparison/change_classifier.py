"""
==========================================================
Change Classifier

Purpose
-------
Determines the change status for a matched parameter.

Responsibilities
----------------
✓ Added
✓ Removed
✓ Modified
✓ Unchanged
✓ Generate Difference Summary
This class DOES NOT

✗ Assign business impact
✗ Match parameters
✗ Generate reports

==========================================================
"""

from v2.models.comparison_item import ComparisonItem

from v2.comparison.difference_engine import DifferenceEngine


class ChangeClassifier:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.difference_engine = DifferenceEngine()

    # ======================================================
    # Public
    # ======================================================

    def classify(self, match):

        parameter_v1 = match["v1"]

        parameter_v2 = match["v2"]

        item = ComparisonItem()

        # ==================================================
        # Added
        # ==================================================

        if parameter_v1 is None:

            item.status = "Added"

            item.parameter_name = ""

            item.matched_parameter = parameter_v2.name

            item.old_value = ""

            item.new_value = parameter_v2.value

            item.category = parameter_v2.category

            item.section = parameter_v2.section

            item.page_v2 = parameter_v2.page_number

            item.confidence_v2 = parameter_v2.confidence

            item.reason = "Parameter introduced in Version 2."

            item.difference_summary = self.difference_engine.compare(
                "",
                parameter_v2.value
            )

            return item

        # ==================================================
        # Removed
        # ==================================================

        if parameter_v2 is None:

            item.status = "Removed"

            item.parameter_name = parameter_v1.name

            item.matched_parameter = ""

            item.old_value = parameter_v1.value

            item.new_value = ""

            item.category = parameter_v1.category

            item.section = parameter_v1.section

            item.page_v1 = parameter_v1.page_number

            item.confidence_v1 = parameter_v1.confidence

            item.reason = "Parameter removed from Version 2."

            item.difference_summary = self.difference_engine.compare(
                parameter_v1.value,
                ""
            )

            return item

        # ==================================================
        # Matched Parameter
        # ==================================================

        item.parameter_name = parameter_v1.name

        item.matched_parameter = parameter_v2.name

        item.old_value = parameter_v1.value

        item.new_value = parameter_v2.value

        item.category = parameter_v2.category or parameter_v1.category

        item.section = parameter_v2.section or parameter_v1.section

        item.page_v1 = parameter_v1.page_number

        item.page_v2 = parameter_v2.page_number

        item.confidence_v1 = parameter_v1.confidence

        item.confidence_v2 = parameter_v2.confidence

        # ==================================================
        # Difference Summary
        # ==================================================

        item.difference_summary = self.difference_engine.compare(
            parameter_v1.value,
            parameter_v2.value
        )

        # ==================================================
        # Modified / Unchanged
        # ==================================================

        if self._normalize(parameter_v1.value) == self._normalize(parameter_v2.value):

            item.status = "Unchanged"

            item.reason = "Parameter value unchanged."

        else:

            item.status = "Modified"

            item.reason = "Parameter value changed."

        return item
    
    # ======================================================
    # Helpers
    # ======================================================

    def _normalize(self, value):

        if value is None:

            return ""

        return (
            str(value)
            .strip()
            .lower()
            .replace("\n", " ")
        )