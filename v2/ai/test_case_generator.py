"""
==========================================================
Test Case Generator

Purpose
-------
Generates suggested UAT test cases based on
product comparison results.

Responsibilities
----------------
✓ Generate UAT scenarios
✓ Generate Regression Test Cases
✓ Prioritize Testing

This module is rule-based.

==========================================================
"""


class TestCaseGenerator:

    # ======================================================
    # Public
    # ======================================================

    def generate(
        self,
        comparison_result
    ):

        test_cases = []

        test_case_id = 1

        for item in comparison_result.items:

            if item.status.lower() == "unchanged":
                continue

            test_cases.extend(

                self._generate_for_parameter(

                    item,

                    test_case_id

                )

            )

            test_case_id = len(test_cases) + 1

        return test_cases

    # ======================================================
    # Parameter Rules
    # ======================================================

    def _generate_for_parameter(
        self,
        item,
        start_id
    ):

        parameter = item.parameter_name.lower()

        cases = []

        # --------------------------------------------------
        # Death Benefit
        # --------------------------------------------------

        if "death" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify Death Benefit calculation after policy issuance."

                )

            )

            cases.append(

                self._case(

                    start_id + 1,

                    item,

                    "Verify Death Benefit payout across all applicable variants."

                )

            )

        # --------------------------------------------------
        # Maturity Benefit
        # --------------------------------------------------

        elif "maturity" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify Maturity Benefit calculation."

                )

            )

        # --------------------------------------------------
        # Premium
        # --------------------------------------------------

        elif "premium" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify premium calculation."

                )

            )

            cases.append(

                self._case(

                    start_id + 1,

                    item,

                    "Verify all premium payment frequencies."

                )

            )

        # --------------------------------------------------
        # Policy Term
        # --------------------------------------------------

        elif "policy term" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify policy term validation."

                )

            )

        # --------------------------------------------------
        # Age
        # --------------------------------------------------

        elif "age" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify minimum age validation."

                )

            )

            cases.append(

                self._case(

                    start_id + 1,

                    item,

                    "Verify maximum age validation."

                )

            )

        # --------------------------------------------------
        # Sum Assured
        # --------------------------------------------------

        elif "sum assured" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify Sum Assured validation."

                )

            )

        # --------------------------------------------------
        # Loan
        # --------------------------------------------------

        elif "loan" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify Policy Loan eligibility."

                )

            )

        # --------------------------------------------------
        # Surrender
        # --------------------------------------------------

        elif "surrender" in parameter:

            cases.append(

                self._case(

                    start_id,

                    item,

                    "Verify surrender benefit calculation."

                )

            )

        # --------------------------------------------------
        # Default
        # --------------------------------------------------

        else:

            cases.append(

                self._case(

                    start_id,

                    item,

                    f"Verify changes for '{item.parameter_name}'."

                )

            )

        return cases

    # ======================================================
    # Helper
    # ======================================================

    def _case(
        self,
        tc_id,
        item,
        description
    ):

        return {

            "test_case_id": f"TC-{tc_id:04}",

            "parameter": item.parameter_name,

            "status": item.status,

            "impact": item.impact,

            "priority": self._priority(item),

            "description": description,

            "expected_result": "System should behave according to the updated product specification."

        }

    # ======================================================
    # Priority
    # ======================================================

    def _priority(
        self,
        item
    ):

        impact = item.impact.lower()

        if impact == "high":
            return "High"

        if impact == "medium":
            return "Medium"

        return "Low"