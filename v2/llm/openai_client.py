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

from v2.config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)


class OpenAIClient:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        if not OPENAI_API_KEY:

            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    # ======================================================
    # Generic Prompt
    # ======================================================

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Sends any prompt to the LLM and returns
        the raw response text.
        """

        response = self.client.responses.create(

            model=OPENAI_MODEL,

            input=prompt,

            temperature=TEMPERATURE,

            max_output_tokens=MAX_TOKENS

        )

        return response.output_text.strip()

    # ======================================================
    # Chat Alias
    # ======================================================

    def chat(
        self,
        prompt: str
    ) -> str:
        """
        Alias for generate().

        Keeps the interface readable for future
        AI modules such as:

        - Business Summary Generator
        - Test Case Generator
        - Compliance Analyzer
        - Impact Reasoner
        """

        return self.generate(prompt)

    # ======================================================
    # Health Check
    # ======================================================

    def test_connection(self):

        try:

            return self.generate(
                "Reply with only the word SUCCESS."
            )

        except Exception as error:

            raise RuntimeError(

                f"OpenAI connection failed: {error}"

            )