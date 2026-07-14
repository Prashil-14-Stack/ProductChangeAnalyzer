"""
==========================================================
Prompt Builder

Purpose
-------
Builds prompts for GPT by injecting document content
into reusable prompt templates.

Responsibilities

✓ Load prompt templates
✓ Inject document text
✓ Return final prompt

This class NEVER calls OpenAI.

==========================================================
"""

from pathlib import Path


class PromptBuilder:

    # ======================================================
    # Prompt Files
    # ======================================================

    EXTRACTION_PROMPT = "product_extraction_prompt.txt"

    COMPARISON_PROMPT = "comparison_prompt.txt"

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, prompts_folder):

        self.prompts_folder = Path(prompts_folder)

    # ======================================================
    # Public Methods
    # ======================================================

    def build_extraction_prompt(
        self,
        document_text
    ):

        template = self._load_template(

            self.EXTRACTION_PROMPT

        )

        return template.replace(

            "{{DOCUMENT_TEXT}}",

            document_text

        )

    # ------------------------------------------------------

    def build_comparison_prompt(
        self,
        changed_parameters
    ):

        template = self._load_template(

            self.COMPARISON_PROMPT

        )

        return template.replace(

            "{{CHANGED_PARAMETERS}}",

            changed_parameters

        )

    # ======================================================
    # Private Methods
    # ======================================================

    def _load_template(
        self,
        filename
    ):

        path = self.prompts_folder / filename

        if not path.exists():

            raise FileNotFoundError(

                f"Prompt template not found: {filename}"

            )

        return path.read_text(
            encoding="utf-8"
        )
    
    # ======================================================
    # Generic Template Loader
    # ======================================================

    def load_template(
        self,
        filename
    ):

        return self._load_template(
            filename
        )