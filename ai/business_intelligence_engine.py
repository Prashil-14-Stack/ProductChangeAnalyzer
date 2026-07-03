from models.business_change import BusinessChange
from models.business_analysis import BusinessAnalysis

from services.llm_service import LLMService


class BusinessIntelligenceEngine:

    """
    Enterprise Business Intelligence Engine

    Converts a BusinessChange into actionable
    business insights using LLM reasoning.
    """

    def __init__(self):

        self.llm = LLMService()

    # ==========================================================
    # Generate Business Intelligence
    # ==========================================================

    def analyze(

        self,

        change: BusinessChange

    ) -> BusinessAnalysis:

        # ------------------------------------------------------
        # Backward Compatibility
        # ------------------------------------------------------

        if change.source_parameter is not None:

            change.parameter = change.source_parameter.name

            change.old_text = change.source_parameter.value

            change.old_value = change.source_parameter.value

        if change.target_parameter is not None:

            change.matched_parameter = change.target_parameter.name

            change.new_text = change.target_parameter.value

            change.new_value = change.target_parameter.value

        # ------------------------------------------------------
        # Generate Business Analysis
        # ------------------------------------------------------

        result = self.llm.generate_business_analysis(

            change

        )

        # ------------------------------------------------------
        # Convert into BusinessAnalysis
        # ------------------------------------------------------

        analysis = BusinessAnalysis(

            summary=result.get(

                "summary",

                ""

            ),

            business_impact=result.get(

                "business_impact",

                ""

            ),

            affected_teams=result.get(

                "affected_teams",

                []

            ),

            stakeholders=result.get(

                "stakeholders",

                []

            ),

            testing_recommendations=result.get(

                "testing_recommendations",

                []

            ),

            regression_required=result.get(

                "regression_required",

                False

            ),

            uat_required=result.get(

                "uat_required",

                False

            ),

            actuarial_review=result.get(

                "actuarial_review",

                False

            ),

            compliance_review=result.get(

                "compliance_review",

                False

            ),

            legal_review=result.get(

                "legal_review",

                False

            ),

            operations_review=result.get(

                "operations_review",

                False

            ),

            migration_impact=result.get(

                "migration_impact",

                False

            ),

            customer_communication_required=result.get(

                "customer_communication_required",

                False

            ),

            risk=result.get(

                "risk",

                "Unknown"

            ),

            priority=result.get(

                "priority",

                "Medium"

            ),

            confidence=result.get(

                "confidence",

                0

            ),

            recommendations=result.get(

                "recommendations",

                []

            ),

            assumptions=result.get(

                "assumptions",

                []

            ),

            notes=result.get(

                "notes",

                []

            )

        )

        return analysis