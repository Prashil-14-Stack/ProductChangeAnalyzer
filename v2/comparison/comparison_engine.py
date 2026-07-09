"""
==========================================================
Comparison Engine

Purpose
-------
Orchestrates comparison between two ProductSpecification
objects.

Workflow
--------
Specification V1
        │
        ▼
Parameter Matcher
        │
        ▼
Change Classifier
        │
        ▼
Impact Analyzer
        │
        ▼
Comparison Summary
        │
        ▼
ComparisonResult

==========================================================
"""

from comparison.parameter_matcher import ParameterMatcher
from comparison.change_classifier import ChangeClassifier
from comparison.impact_analyzer import ImpactAnalyzer
from comparison.comparison_summary import ComparisonSummary

from models.comparison_result import ComparisonResult


class ComparisonEngine:

    """
    Main orchestration class for comparison.
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.matcher = ParameterMatcher()

        self.classifier = ChangeClassifier()

        self.impact = ImpactAnalyzer()

        self.summary = ComparisonSummary()

    # ======================================================
    # Compare Specifications
    # ======================================================

    def compare(
        self,
        specification_v1,
        specification_v2
    ):

        print()
        print("=" * 80)
        print("STARTING PRODUCT COMPARISON")
        print("=" * 80)

        # --------------------------------------------------
        # Match Parameters
        # --------------------------------------------------

        matched_parameters = self.matcher.match(
            specification_v1,
            specification_v2
        )

        print(
            f"Matched Parameters : {len(matched_parameters)}"
        )

        # --------------------------------------------------
        # Classify Changes
        # --------------------------------------------------

        comparison_items = []

        for match in matched_parameters:

            comparison = self.classifier.classify(match)

            comparison = self.impact.analyze(
                comparison
            )

            comparison_items.append(
                comparison
            )

        # --------------------------------------------------
        # Build Result
        # --------------------------------------------------

        result = ComparisonResult()

        result.product_name_v1 = specification_v1.product_name

        result.product_name_v2 = specification_v2.product_name

        result.items = comparison_items

        result.summary = self.summary.generate(
            comparison_items
        )

        print()
        print("=" * 80)
        print("COMPARISON COMPLETED")
        print("=" * 80)

        print(f"Compared Items : {len(comparison_items)}")

        return result