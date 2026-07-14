"""
==========================================================
Recommendation Engine

Purpose
-------
Generates actionable business recommendations
based on comparison results.

Responsibilities
----------------
✓ Product Recommendations
✓ QA Recommendations
✓ Compliance Recommendations
✓ Operations Recommendations
✓ Business Recommendations

This module is deterministic and rule-based.

==========================================================
"""


class RecommendationEngine:

    # ======================================================
    # Public
    # ======================================================

    def generate(
        self,
        comparison_result
    ):

        recommendations = []

        seen = set()

        for item in comparison_result.items:

            if item.status.lower() == "unchanged":
                continue

            actions = self._recommend(item)

            for action in actions:

                key = (

                    action["team"],

                    action["recommendation"]

                )

                if key not in seen:

                    seen.add(key)

                    recommendations.append(action)

        return recommendations

    # ======================================================
    # Rules
    # ======================================================

    def _recommend(
        self,
        item
    ):

        parameter = item.parameter_name.lower()

        actions = []

        # --------------------------------------------------
        # Benefits
        # --------------------------------------------------

        if any(

            keyword in parameter

            for keyword in [

                "death",

                "maturity",

                "income",

                "benefit",

                "surrender"

            ]

        ):

            actions.extend([

                self._action(

                    "Product Team",

                    "Review benefit configuration."

                ),

                self._action(

                    "QA",

                    "Execute regression testing for benefit calculations."

                ),

                self._action(

                    "Actuarial",

                    "Validate benefit calculations."

                )

            ])

        # --------------------------------------------------
        # Eligibility
        # --------------------------------------------------

        if any(

            keyword in parameter

            for keyword in [

                "age",

                "policy term",

                "sum assured",

                "eligibility"

            ]

        ):

            actions.extend([

                self._action(

                    "Business Analyst",

                    "Review eligibility rules."

                ),

                self._action(

                    "Product Team",

                    "Update product configuration."

                ),

                self._action(

                    "QA",

                    "Validate boundary conditions."

                )

            ])

        # --------------------------------------------------
        # Premium
        # --------------------------------------------------

        if "premium" in parameter:

            actions.extend([

                self._action(

                    "Finance",

                    "Validate premium calculations."

                ),

                self._action(

                    "QA",

                    "Verify all payment frequencies."

                )

            ])

        # --------------------------------------------------
        # Options
        # --------------------------------------------------

        if any(

            keyword in parameter

            for keyword in [

                "option",

                "instalment",

                "frequency"

            ]

        ):

            actions.extend([

                self._action(

                    "Operations",

                    "Review servicing process."

                ),

                self._action(

                    "QA",

                    "Verify customer option journeys."

                )

            ])

        # --------------------------------------------------
        # Compliance
        # --------------------------------------------------

        if any(

            keyword in parameter

            for keyword in [

                "tax",

                "free look",

                "grace",

                "revival",

                "regulatory"

            ]

        ):

            actions.append(

                self._action(

                    "Compliance",

                    "Review regulatory implications."

                )

            )

        # --------------------------------------------------
        # Default
        # --------------------------------------------------

        if not actions:

            actions.append(

                self._action(

                    "Business Analyst",

                    f"Review change for '{item.parameter_name}'."

                )

            )

        return actions

    # ======================================================
    # Helper
    # ======================================================

    def _action(
        self,
        team,
        recommendation
    ):

        return {

            "team": team,

            "recommendation": recommendation

        }