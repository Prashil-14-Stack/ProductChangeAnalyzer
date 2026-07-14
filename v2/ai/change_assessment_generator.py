"""
==========================================================
Change Assessment Generator

Purpose
-------
Uses GPT to generate business impact analysis for
each changed parameter.

==========================================================
"""

import json

from v2.llm.prompt_builder import PromptBuilder
from v2.llm.openai_client import OpenAIClient
from v2.models.change_assessment import ChangeAssessment
from v2.config.settings import PROMPTS_FOLDER


class ChangeAssessmentGenerator:

    def __init__(self):

        self.prompt_builder = PromptBuilder(
            PROMPTS_FOLDER
        )

        self.client = OpenAIClient()

    # ======================================================
    # Public
    # ======================================================

    def generate(
        self,
        item
    ):

        prompt = self._build_prompt(
            item
        )

        response = self.client.generate(
            prompt
        )

        print("\n")
        print("=" * 80)
        print("AI CHANGE ASSESSMENT RAW RESPONSE")
        print("=" * 80)
        print(response)
        print("=" * 80)

        return self._parse_response(
            response
        )
    # ======================================================
    # Prompt Builder
    # ======================================================

    def _build_prompt(
        self,
        item
    ):

        template = self.prompt_builder.load_template(
            "change_assessment_prompt.txt"
        )

        template = template.replace(
            "{{PARAMETER_NAME}}",
            item.parameter_name
        )

        template = template.replace(
            "{{STATUS}}",
            item.status
        )

        template = template.replace(
            "{{OLD_VALUE}}",
            item.old_value or ""
        )

        template = template.replace(
            "{{NEW_VALUE}}",
            item.new_value or ""
        )

        template = template.replace(
            "{{DIFFERENCE_SUMMARY}}",
            item.difference_summary or "No Difference"
        )

        return template

    # ======================================================
    # Parse GPT Response
    # ======================================================

    def _parse_response(
        self,
        response
    ):

        data = json.loads(response)

        return ChangeAssessment(

            difference_summary=data.get(
                "difference_summary",
                ""
            ),

            executive_summary=data.get(
                "executive_summary",
                ""
            ),

            business_impact=data.get(
                "business_impact",
                ""
            ),

            remarks=data.get(
                "remarks",
                ""
            ),

            risk=data.get(
                "risk",
                ""
            ),

            priority=data.get(
                "priority",
                ""
            ),

            business_criticality=data.get(
                "business_criticality",
                ""
            ),

            testing_recommendation=data.get(
                "testing_recommendation",
                ""
            ),

            affected_teams=data.get(
                "affected_teams",
                []
            )

        )