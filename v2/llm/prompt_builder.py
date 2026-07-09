"""
==========================================================
Prompt Builder

Purpose
-------
Builds prompts for GPT by injecting document content
into reusable prompt templates.

Responsibilities

✓ Load prompt template
✓ Inject document text
✓ Return final prompt

This class NEVER calls OpenAI.

==========================================================
"""

from pathlib import Path


class PromptBuilder:

    def __init__(self, prompts_folder):

        self.prompts_folder = Path(prompts_folder)

    # ======================================================
    # Public Methods
    # ======================================================

    def build_extraction_prompt(self, document_text):

        template = self._load_template(
            "extraction_prompt.txt"
        )

        return template.replace(

            "{{DOCUMENT_TEXT}}",

            document_text

        )

    # ------------------------------------------------------

    def build_comparison_prompt(self, changed_parameters):

        template = self._load_template(
            "comparison_prompt.txt"
        )

        return template.replace(

            "{{CHANGED_PARAMETERS}}",

            changed_parameters

        )

    # ======================================================
    # Private Methods
    # ======================================================

    def _load_template(self, filename):

        path = self.prompts_folder / filename

        if not path.exists():

            raise FileNotFoundError(

                f"Prompt template not found: {filename}"

            )

        return path.read_text(
            encoding="utf-8"
        )