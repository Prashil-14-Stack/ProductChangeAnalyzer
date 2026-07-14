"""
==========================================================
Risk Assessor

Purpose
-------
Calculates the overall business risk associated
with product changes.

Responsibilities
----------------
✓ Calculate Overall Risk Score
✓ Assign Risk Level
✓ Identify High-Risk Parameters
✓ Generate Risk Summary

This module is deterministic and rule-based.

==========================================================
"""


class RiskAssessor:

    # ======================================================
    # Risk Weights
    # ======================================================

    PARAMETER_WEIGHTS = {

        "death": 30,
        "maturity": 25,
        "income": 20,
        "benefit": 20,
        "premium": 20,
        "sum assured": 20,
        "eligibility": 15,
        "age": 15,
        "policy term": 15,
        "loan": 10,
        "surrender": 15,
        "grace": 10,
        "revival": 10,
        "tax": 15,
        "option": 5,
        "frequency": 5

    }

    STATUS_MULTIPLIER = {

        "added": 1.0,

        "modified": 1.5,

        "removed": 2.0,

        "unchanged": 0.0

    }

    # ======================================================
    # Public
    # ======================================================

    def assess(
        self,
        comparison_result
    ):

        total_score = 0

        high_risk_parameters = []

        parameter_scores = []

        for item in comparison_result.items:

            score = self._score(item)

            parameter_scores.append({

                "parameter": item.parameter_name,

                "score": score,

                "status": item.status,

                "impact": item.impact

            })

            total_score += score

            if score >= 30:

                high_risk_parameters.append(

                    item.parameter_name

                )

        return {

            "overall_score": total_score,

            "overall_risk": self._risk_level(total_score),

            "high_risk_parameters": sorted(

                list(set(high_risk_parameters))

            ),

            "parameter_scores": sorted(

                parameter_scores,

                key=lambda x: x["score"],

                reverse=True

            )

        }

    # ======================================================
    # Scoring
    # ======================================================

    def _score(
        self,
        item
    ):

        parameter = (item.parameter_name or "").lower()

        base_score = 5

        for keyword, weight in self.PARAMETER_WEIGHTS.items():

            if keyword in parameter:

                base_score = max(

                    base_score,

                    weight

                )

        multiplier = self.STATUS_MULTIPLIER.get(

            item.status.lower(),

            1.0

        )

        return round(

            base_score * multiplier

        )

    # ======================================================
    # Risk Level
    # ======================================================

    def _risk_level(
        self,
        score
    ):

        if score >= 150:

            return "Critical"

        if score >= 100:

            return "High"

        if score >= 50:

            return "Medium"

        return "Low"