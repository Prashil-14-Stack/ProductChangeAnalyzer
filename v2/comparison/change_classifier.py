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

This class DOES NOT

✗ Assign business impact
✗ Match parameters
✗ Generate reports

==========================================================
"""

from models.comparison_item import ComparisonItem


class ChangeClassifier:

    """
    Classifies the change status of matched parameters.
    """

    # ======================================================
    # Public
    # ======================================================

    def classify(self, match):

        parameter_v1 = match["v1"]

        parameter_v2 = match["v2"]

        item = ComparisonItem()

        # --------------------------------------------------
        # Parameter Name
        # --------------------------------------------------

        item.parameter_name = match["parameter_name"]

        # --------------------------------------------------
        # Added
        # --------------------------------------------------

        if parameter_v1 is None:

            item.status = "Added"

            item.new_value = parameter_v2.value

            item.category = parameter_v2.category

            item.section = parameter_v2.section

            item.page_v2 = parameter_v2.page_number

            item.confidence_v2 = parameter_v2.confidence

            item.reason = "Parameter introduced in Version 2."

            return item

        # --------------------------------------------------
        # Removed
        # --------------------------------------------------

        if parameter_v2 is None:

            item.status = "Removed"

            item.old_value = parameter_v1.value

            item.category = parameter_v1.category

            item.section = parameter_v1.section

            item.page_v1 = parameter_v1.page_number

            item.confidence_v1 = parameter_v1.confidence

            item.reason = "Parameter removed from Version 2."

            return item

        # --------------------------------------------------
        # Common Information
        # --------------------------------------------------

        item.old_value = parameter_v1.value

        item.new_value = parameter_v2.value

        item.category = parameter_v2.category or parameter_v1.category

        item.section = parameter_v2.section or parameter_v1.section

        item.page_v1 = parameter_v1.page_number

        item.page_v2 = parameter_v2.page_number

        item.confidence_v1 = parameter_v1.confidence

        item.confidence_v2 = parameter_v2.confidence

        # --------------------------------------------------
        # Modified / Unchanged
        # --------------------------------------------------

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