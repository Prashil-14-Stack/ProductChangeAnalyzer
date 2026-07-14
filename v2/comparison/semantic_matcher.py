"""
==========================================================
Semantic Matcher

Purpose
-------
Uses the LLM to determine which candidate parameter
represents the same business meaning.

Responsibilities
----------------
✓ Semantic parameter matching
✓ Business meaning comparison
✓ Confidence scoring
✓ Explanation generation

This class DOES NOT

✗ Compare documents
✗ Classify changes
✗ Calculate impact

==========================================================
"""

import json
from pathlib import Path

from v2.llm.openai_client import OpenAIClient


class SemanticMatcher:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.client = OpenAIClient()

        base_dir = Path(__file__).resolve().parent.parent

        prompt_path = (
            base_dir
            / "prompts"
            / "semantic_matching_prompt.txt"
        )

        self.prompt_template = prompt_path.read_text(
            encoding="utf-8"
        )

    # ======================================================
    # Public
    # ======================================================

    def find_best_match(
        self,
        source_parameter,
        candidate_parameters
    ):

        """
        Returns the best semantic match for a parameter.
        """

        if not candidate_parameters:

            return None

        prompt = self._build_prompt(

            source_parameter,

            candidate_parameters

        )

        response = self.client.generate(prompt)

        return self._parse_response(

            response,

            candidate_parameters

        )

    # ======================================================
    # Prompt Builder
    # ======================================================

    def _build_prompt(

        self,

        source_parameter,

        candidates

    ):

        candidate_text = []

        for index, parameter in enumerate(

            candidates,

            start=1

        ):

            candidate_text.append(

                f"""
Candidate {index}

Name:
{parameter.name}

Category:
{parameter.category}

Section:
{parameter.section}

Value:
{parameter.value}
""".strip()

            )

        prompt = self.prompt_template

        prompt = prompt.replace(

            "{{SOURCE_PARAMETER}}",

            f"""
Name:
{source_parameter.name}

Category:
{source_parameter.category}

Section:
{source_parameter.section}

Value:
{source_parameter.value}
""".strip()

        )

        prompt = prompt.replace(

            "{{CANDIDATES}}",

            "\n\n".join(candidate_text)

        )

        return prompt

    # ======================================================
    # Response Parser
    # ======================================================

    def _parse_response(

        self,

        response,

        candidates

    ):

        try:

            result = json.loads(response)

        except Exception:

            return None

        if not result.get("matched"):

            return None

        index = result.get("candidate_number")

        if index is None:

            return None

        if index < 1 or index > len(candidates):

            return None

        return {

            "parameter": candidates[index - 1],

            "confidence": result.get(

                "confidence",

                0.0

            ),

            "reason": result.get(

                "reason",

                ""

            )

        }