"""
==========================================================
Business Summary Generator

Purpose
-------
Generates an AI-powered executive business summary from
a ComparisonResult.

Responsibilities
----------------
✓ Build comparison summary prompt
✓ Call OpenAI
✓ Return executive summary

This class DOES NOT

✗ Read PDFs
✗ Compare products
✗ Parse JSON

==========================================================
"""

from pathlib import Path

from v2.llm.openai_client import OpenAIClient


class BusinessSummaryGenerator:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.client = OpenAIClient()

        prompt_file = (
            Path(__file__).parent /
            "summary_prompt.txt"
        )

        self.prompt_template = prompt_file.read_text(
            encoding="utf-8"
        )

    # ======================================================
    # Public
    # ======================================================

    def generate(
        self,
        comparison_result
    ) -> str:

        comparison_text = self._build_comparison_text(
            comparison_result
        )

        prompt = self.prompt_template.replace(
            "{{comparison}}",
            comparison_text
        )

        return self.client.generate(prompt)

    # ======================================================
    # Helpers
    # ======================================================

    def _build_comparison_text(
        self,
        comparison_result
    ):

        lines = []

        # --------------------------------------------------
        # Product Information
        # --------------------------------------------------

        lines.append("PRODUCT INFORMATION")
        lines.append("-------------------")

        lines.append(
            f"Product V1: {comparison_result.product_name_v1}"
        )

        lines.append(
            f"Product V2: {comparison_result.product_name_v2}"
        )

        lines.append("")

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        lines.append("SUMMARY")
        lines.append("-------")

        for key, value in comparison_result.summary.items():

            lines.append(
                f"{key}: {value}"
            )

        lines.append("")

        # --------------------------------------------------
        # Detailed Changes
        # --------------------------------------------------

        lines.append("DETAILED CHANGES")
        lines.append("----------------")

        for item in comparison_result.items:

            lines.append(
                f"""
Parameter : {item.parameter_name}
Status    : {item.status}
Impact    : {item.impact}
Category  : {item.category}
Section   : {item.section}
Old Value : {item.old_value}
New Value : {item.new_value}
Reason    : {item.reason}
""".strip()
            )

            lines.append("")

        return "\n".join(lines)