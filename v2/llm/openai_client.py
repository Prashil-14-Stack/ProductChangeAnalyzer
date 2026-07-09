"""
==========================================================
OpenAI Client

Purpose
-------
Handles communication with the OpenAI API.

Responsibilities
----------------
✓ Connect to OpenAI
✓ Submit prompts
✓ Return raw response text

This class DOES NOT

✗ Build prompts
✗ Parse JSON
✗ Compare products
✗ Generate reports

==========================================================
"""

from openai import OpenAI

from config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)


class OpenAIClient:

    def __init__(self):

        if not OPENAI_API_KEY:

            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    # ======================================================
    # Extract Product Specification
    # ======================================================

    def generate(self, prompt: str) -> str:

        """
        Sends a prompt to OpenAI and returns
        the raw text response.
        """

        response = self.client.responses.create(

            model=OPENAI_MODEL,

            input=prompt,

            temperature=TEMPERATURE,

            max_output_tokens=MAX_TOKENS

        )

        return response.output_text

    # ======================================================
    # Health Check
    # ======================================================

    def test_connection(self):

        try:

            response = self.client.responses.create(

                model=OPENAI_MODEL,

                input="Reply with the word SUCCESS."

            )

            return response.output_text.strip()

        except Exception as error:

            raise RuntimeError(

                f"OpenAI connection failed: {error}"

            )