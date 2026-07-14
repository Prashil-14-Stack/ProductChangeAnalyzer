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
AI Change Assessment
        │
        ▼
Comparison Summary
        │
        ▼
ComparisonResult

==========================================================
"""

from v2.comparison.parameter_matcher import ParameterMatcher
from v2.comparison.change_classifier import ChangeClassifier
from v2.comparison.impact_analyzer import ImpactAnalyzer
from v2.comparison.comparison_summary import ComparisonSummary

from v2.models.comparison_result import ComparisonResult

from v2.ai.change_assessment_generator import ChangeAssessmentGenerator


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

        self.change_assessment = ChangeAssessmentGenerator()

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

            # ------------------------------------------
            # Classify
            # ------------------------------------------

            comparison = self.classifier.classify(
                match
            )

            # ------------------------------------------
            # Impact Analysis
            # ------------------------------------------

            comparison = self.impact.analyze(
                comparison
            )

            # ------------------------------------------
            # AI Change Assessment
            # ------------------------------------------

            try:

                assessment = self.change_assessment.generate(
                    comparison
                )

                if assessment is None:

                    raise RuntimeError(
                        "ChangeAssessmentGenerator returned None."
                    )

                comparison.summary = getattr(
                    assessment,
                    "executive_summary",
                    ""
                )

                comparison.business_impact = getattr(
                    assessment,
                    "business_impact",
                    ""
                )

                comparison.remarks = getattr(
                    assessment,
                    "remarks",
                    ""
                )

                comparison.risk = getattr(
                    assessment,
                    "risk",
                    ""
                )

                comparison.priority = getattr(
                    assessment,
                    "priority",
                    ""
                )

                comparison.business_criticality = getattr(
                    assessment,
                    "business_criticality",
                    ""
                )

                comparison.testing_recommendation = getattr(
                    assessment,
                    "testing_recommendation",
                    ""
                )

                affected = getattr(
                    assessment,
                    "affected_teams",
                    []
                )

                if isinstance(affected, list):

                    comparison.affected_teams = ", ".join(
                        affected
                    )

                else:

                    comparison.affected_teams = str(
                        affected
                    )

                comparison.difference_summary = getattr(
                    assessment,
                    "difference_summary",
                    comparison.difference_summary
                )

            except Exception:

                import traceback

                print("\n" + "=" * 80)
                print("AI CHANGE ASSESSMENT FAILED")
                print("=" * 80)

                traceback.print_exc()

                raise

            # ------------------------------------------
            # IMPORTANT: Store the comparison item
            # ------------------------------------------

            comparison_items.append(
                comparison
            )

            print(
                f"Added: {comparison.parameter_name} | "
                f"{comparison.status} | "
                f"Total Items: {len(comparison_items)}"
            )
        # --------------------------------------------------
        # Build Result
        # --------------------------------------------------

        result = ComparisonResult()

        result.product_name_v1 = specification_v1.product_name

        result.product_name_v2 = specification_v2.product_name

        result.version_v1 = getattr(
            specification_v1,
            "product_version",
            ""
        )

        result.version_v2 = getattr(
            specification_v2,
            "product_version",
            ""
        )

        result.items = comparison_items

        result.summary = self.summary.generate(
            comparison_items
        )

        print()

        print("=" * 80)

        print("COMPARISON COMPLETED")

        print("=" * 80)

        print(
            f"Compared Items : {len(comparison_items)}"
        )

        return result