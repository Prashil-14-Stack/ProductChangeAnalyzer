"""
==========================================================
Impact Analyzer

Purpose
-------
Analyzes product changes and determines business
impact across multiple business functions.

Responsibilities
----------------
✓ Product Configuration Impact
✓ UAT Impact
✓ Compliance Impact
✓ Operations Impact
✓ Actuarial Impact
✓ Customer Impact

This module is rule-based.

It does NOT call GPT.

==========================================================
"""

from collections import defaultdict


class ImpactAnalyzer:

    # ======================================================
    # Public
    # ======================================================

    def analyze(
        self,
        comparison_result
    ):

        impacts = {

            "product_configuration": [],

            "uat": [],

            "compliance": [],

            "operations": [],

            "actuarial": [],

            "customer": []

        }

        for item in comparison_result.items:

            if item.status.lower() == "unchanged":

                continue

            self._classify(
                item,
                impacts
            )

        return impacts

    # ======================================================
    # Classification
    # ======================================================

    def _classify(
        self,
        item,
        impacts
    ):

        category = (item.category or "").lower()

        parameter = (item.parameter_name or "").lower()

        # --------------------------------------------------
        # Product Configuration
        # --------------------------------------------------

        if category in [

            "product configuration",

            "eligibility",

            "premium",

            "policy",

            "options"

        ]:

            impacts["product_configuration"].append(

                item.parameter_name

            )

        # --------------------------------------------------
        # UAT
        # --------------------------------------------------

        if item.status.lower() in [

            "modified",

            "added",

            "removed"

        ]:

            impacts["uat"].append(

                item.parameter_name

            )

        # --------------------------------------------------
        # Compliance
        # --------------------------------------------------

        compliance_keywords = [

            "tax",

            "eligibility",

            "age",

            "regulatory",

            "grace",

            "revival",

            "free look",

            "surrender"

        ]

        if any(

            keyword in parameter

            for keyword in compliance_keywords

        ):

            impacts["compliance"].append(

                item.parameter_name

            )

        # --------------------------------------------------
        # Operations
        # --------------------------------------------------

        operations_keywords = [

            "payment",

            "frequency",

            "loan",

            "options",

            "instalment",

            "policy"

        ]

        if any(

            keyword in parameter

            for keyword in operations_keywords

        ):

            impacts["operations"].append(

                item.parameter_name

            )

        # --------------------------------------------------
        # Actuarial
        # --------------------------------------------------

        actuarial_keywords = [

            "benefit",

            "premium",

            "sum assured",

            "death",

            "maturity",

            "income"

        ]

        if any(

            keyword in parameter

            for keyword in actuarial_keywords

        ):

            impacts["actuarial"].append(

                item.parameter_name

            )

        # --------------------------------------------------
        # Customer
        # --------------------------------------------------

        customer_keywords = [

            "benefit",

            "age",

            "policy",

            "payment",

            "option",

            "term"

        ]

        if any(

            keyword in parameter

            for keyword in customer_keywords

        ):

            impacts["customer"].append(

                item.parameter_name

            )

    # ======================================================
    # Summary
    # ======================================================

    def summarize(
        self,
        impacts
    ):

        summary = {}

        for area, items in impacts.items():

            summary[area] = {

                "count": len(items),

                "parameters": sorted(

                    list(

                        set(items)

                    )

                )

            }

        return summary