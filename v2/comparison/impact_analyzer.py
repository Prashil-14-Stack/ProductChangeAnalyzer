"""
==========================================================
Impact Analyzer

Purpose
-------
Assign business impact to comparison items.

Responsibilities
----------------
✓ Assign High / Medium / Low impact
✓ Populate reason where appropriate

This class DOES NOT

✗ Compare parameters
✗ Call GPT
✗ Generate reports

==========================================================
"""


class ImpactAnalyzer:

    """
    Assigns business impact based on parameter name
    and change status.
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.high_impact_parameters = {

            "death benefit",

            "maturity benefit",

            "sum assured",

            "premium",

            "premium payment term",

            "policy term",

            "minimum entry age",

            "maximum entry age",

            "minimum maturity age",

            "maximum maturity age",

            "loan",

            "surrender benefit",

            "grace period",

            "revival",

            "free look period"

        }

        self.medium_impact_parameters = {

            "premium payment frequency",

            "income benefit",

            "lumpsum benefit at maturity",

            "variant",

            "variants",

            "options available under the product"

        }

    # ======================================================
    # Public
    # ======================================================

    def analyze(self, comparison_item):

        parameter = comparison_item.parameter_name.strip().lower()

        # -----------------------------------------------
        # Unchanged
        # -----------------------------------------------

        if comparison_item.status == "Unchanged":

            comparison_item.impact = "None"

            return comparison_item

        # -----------------------------------------------
        # High Impact
        # -----------------------------------------------

        if parameter in self.high_impact_parameters:

            comparison_item.impact = "High"

            if not comparison_item.reason:

                comparison_item.reason = (
                    "Core insurance parameter changed."
                )

            return comparison_item

        # -----------------------------------------------
        # Medium Impact
        # -----------------------------------------------

        if parameter in self.medium_impact_parameters:

            comparison_item.impact = "Medium"

            if not comparison_item.reason:

                comparison_item.reason = (
                    "Business functionality may be affected."
                )

            return comparison_item

        # -----------------------------------------------
        # Default
        # -----------------------------------------------

        comparison_item.impact = "Low"

        if not comparison_item.reason:

            comparison_item.reason = (
                "Cosmetic or informational change."
            )

        return comparison_item