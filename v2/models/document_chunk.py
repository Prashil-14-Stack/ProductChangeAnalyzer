"""
==========================================================
Document Chunk Model

Purpose
-------
Represents a chunk of a document that will be sent
to the LLM.

==========================================================
"""

from dataclasses import dataclass


@dataclass
class DocumentChunk:

    chunk_id: int

    start_page: int

    end_page: int

    text: str

    def page_range(self):

        return f"{self.start_page}-{self.end_page}"

    def word_count(self):

        return len(self.text.split())

    def __str__(self):

        return (

            f"Chunk {self.chunk_id} "

            f"({self.start_page}-{self.end_page})"

        )