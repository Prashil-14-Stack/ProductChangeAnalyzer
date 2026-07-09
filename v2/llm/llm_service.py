"""
==========================================================
LLM Service

Purpose
-------
Enterprise orchestration layer for all LLM operations.

Workflow
--------
Document
    ↓
DocumentChunker
    ↓
Prompt Builder
    ↓
OpenAI Client
    ↓
Response Parser
    ↓
Specification Merger
    ↓
ProductSpecification

==========================================================
"""

import json

from llm.prompt_builder import PromptBuilder
from llm.openai_client import OpenAIClient
from llm.response_parser import ResponseParser
from llm.specification_merger import SpecificationMerger

from readers.document_chunker import DocumentChunker

from config.settings import (
    PROMPTS_FOLDER,
    JSON_RETRY_COUNT
)


class LLMService:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.prompt_builder = PromptBuilder(
            PROMPTS_FOLDER
        )

        self.client = OpenAIClient()

        self.parser = ResponseParser()

        self.chunker = DocumentChunker()

        self.merger = SpecificationMerger()

    # ======================================================
    # Health Check
    # ======================================================

    def health_check(self):

        return self.client.test_connection()

    # ======================================================
    # Extract Product Specification
    # ======================================================

    def extract_product_specification(
        self,
        document
    ):

        chunks = self.chunker.create_chunks(
            document
        )

        specifications = []

        print()

        print("=" * 80)
        print("LLM EXTRACTION")
        print("=" * 80)

        print(f"Chunks to Process : {len(chunks)}")

        for chunk in chunks:

            print()

            print(
                f"Processing Chunk "
                f"{chunk.chunk_id} "
                f"(Pages "
                f"{chunk.start_page}-{chunk.end_page})"
            )

            specification = self._process_chunk(
                chunk
            )

            specifications.append(
                specification
            )

        print()

        print("Merging extracted specifications...")

        merged = self.merger.merge(
            specifications
        )

        return merged

    # ======================================================
    # Process One Chunk
    # ======================================================

    def _process_chunk(
        self,
        chunk
    ):

        prompt = self.prompt_builder.build_extraction_prompt(
            chunk.text
        )

        last_error = None

        for attempt in range(
            JSON_RETRY_COUNT
        ):

            try:

                response = self.client.generate(
                    prompt
                )

                if not self.parser.validate_json(
                    response
                ):

                    raise ValueError(
                        "Invalid JSON returned by GPT."
                    )

                specification = self.parser.parse_product_specification(
                    response
                )

                return specification

            except Exception as error:

                last_error = error

                print(

                    f"Retry "

                    f"{attempt + 1}/"

                    f"{JSON_RETRY_COUNT}"

                )

        raise RuntimeError(

            f"Chunk "

            f"{chunk.chunk_id}"

            f" failed.\n"

            f"{last_error}"

        )

    # ======================================================
    # Business Impact Analysis
    # ======================================================

    def analyze_changes(
        self,
        changed_parameters
    ):

        if isinstance(
            changed_parameters,
            list
        ):

            changed_parameters = json.dumps(

                changed_parameters,

                indent=2,

                ensure_ascii=False

            )

        prompt = self.prompt_builder.build_comparison_prompt(

            changed_parameters

        )

        response = self.client.generate(

            prompt

        )

        return json.loads(

            response

        )

    # ======================================================
    # Generic Prompt
    # ======================================================

    def ask(
        self,
        prompt
    ):

        return self.client.generate(
            prompt
        )