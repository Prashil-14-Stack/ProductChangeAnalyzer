"""
==========================================================
Comparison Summary

Purpose
-------
Generate summary statistics for a completed comparison.

Responsibilities
----------------
✓ Count Added parameters
✓ Count Removed parameters
✓ Count Modified parameters
✓ Count Unchanged parameters
✓ Count High/Medium/Low impact items

This class DOES NOT

✗ Compare parameters
✗ Call GPT
✗ Generate Excel reports

==========================================================
"""


class ComparisonSummary:

    """
    Generates summary statistics from ComparisonItems.
    """

    # ======================================================
    # Public
    # ======================================================

    def generate(self, comparison_items):

        summary = {

            # ----------------------------------------------
            # Overall Counts
            # ----------------------------------------------

            "total_parameters": len(comparison_items),

            "added": 0,

            "removed": 0,

            "modified": 0,

            "unchanged": 0,

            # ----------------------------------------------
            # Impact Counts
            # ----------------------------------------------

            "high_impact": 0,

            "medium_impact": 0,

            "low_impact": 0,

            "no_impact": 0

        }

        # --------------------------------------------------
        # Calculate Statistics
        # --------------------------------------------------

        for item in comparison_items:

            # -------------------------
            # Status
            # -------------------------

            status = item.status.lower()

            if status == "added":

                summary["added"] += 1

            elif status == "removed":

                summary["removed"] += 1

            elif status == "modified":

                summary["modified"] += 1

            elif status == "unchanged":

                summary["unchanged"] += 1

            # -------------------------
            # Impact
            # -------------------------

            impact = item.impact.lower()

            if impact == "high":

                summary["high_impact"] += 1

            elif impact == "medium":

                summary["medium_impact"] += 1

            elif impact == "low":

                summary["low_impact"] += 1

            elif impact == "none":

                summary["no_impact"] += 1

        return summary

    # ======================================================
    # Pretty Print
    # ======================================================

    def print_summary(self, summary):

        print()

        print("=" * 80)

        print("COMPARISON SUMMARY")

        print("=" * 80)

        print(f"Total Parameters : {summary['total_parameters']}")

        print()

        print("Status")

        print("------")

        print(f"Added       : {summary['added']}")

        print(f"Removed     : {summary['removed']}")

        print(f"Modified    : {summary['modified']}")

        print(f"Unchanged   : {summary['unchanged']}")

        print()

        print("Business Impact")

        print("----------------")

        print(f"High Impact   : {summary['high_impact']}")

        print(f"Medium Impact : {summary['medium_impact']}")

        print(f"Low Impact    : {summary['low_impact']}")

        print(f"No Impact     : {summary['no_impact']}")

        print("=" * 80)