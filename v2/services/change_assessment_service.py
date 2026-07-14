"""
==========================================================
Change Assessment Service

Purpose
-------
Orchestrates all business intelligence modules and
produces a complete ChangeAssessment.

Workflow
--------

ComparisonResult
        │
        ▼
Impact Analyzer
        │
        ▼
Risk Assessor
        │
        ▼
Stakeholder Mapper
        │
        ▼
Recommendation Engine
        │
        ▼
Test Case Generator
        │
        ▼
Business Summary Generator
        │
        ▼
ChangeAssessment

==========================================================
"""

from v2.models.change_assessment import ChangeAssessment

from ai.impact_analyzer import ImpactAnalyzer
from ai.risk_assessor import RiskAssessor
from ai.stakeholder_mapper import StakeholderMapper
from ai.recommendation_engine import RecommendationEngine
from ai.test_case_generator import TestCaseGenerator
from ai.business_summary_generator import BusinessSummaryGenerator


class ChangeAssessmentService:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.impact_analyzer = ImpactAnalyzer()

        self.risk_assessor = RiskAssessor()

        self.stakeholder_mapper = StakeholderMapper()

        self.recommendation_engine = RecommendationEngine()

        self.test_case_generator = TestCaseGenerator()

        self.business_summary_generator = BusinessSummaryGenerator()

    # ======================================================
    # Public
    # ======================================================

    def analyze(
        self,
        comparison_result
    ):

        print()

        print("=" * 80)
        print("CHANGE ASSESSMENT")
        print("=" * 80)

        # --------------------------------------------------
        # Impact Analysis
        # --------------------------------------------------

        impacts = self.impact_analyzer.analyze(
            comparison_result
        )

        impact_summary = self.impact_analyzer.summarize(
            impacts
        )

        # --------------------------------------------------
        # Risk Assessment
        # --------------------------------------------------

        risk_summary = self.risk_assessor.assess(
            comparison_result
        )

        # --------------------------------------------------
        # Stakeholder Mapping
        # --------------------------------------------------

        stakeholder_map = self.stakeholder_mapper.map(
            comparison_result
        )

        stakeholder_summary = self.stakeholder_mapper.summarize(
            stakeholder_map
        )

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        recommendations = self.recommendation_engine.generate(
            comparison_result
        )

        # --------------------------------------------------
        # Test Cases
        # --------------------------------------------------

        test_cases = self.test_case_generator.generate(
            comparison_result
        )

        # --------------------------------------------------
        # AI Business Summary
        # --------------------------------------------------

        business_summary = self.business_summary_generator.generate(
            comparison_result
        )

        # --------------------------------------------------
        # Build Assessment
        # --------------------------------------------------

        assessment = ChangeAssessment(

            comparison_result=comparison_result,

            impact_summary=impact_summary,

            risk_summary=risk_summary,

            stakeholder_summary=stakeholder_summary,

            stakeholder_map=stakeholder_map,

            recommendations=recommendations,

            test_cases=test_cases,

            business_summary=business_summary

        )

        return assessment