"""
==========================================================
Document Chunker

Purpose
-------
Split a Document into LLM-friendly chunks.

Responsibilities
----------------
✓ Preserve page boundaries
✓ Respect maximum pages per chunk
✓ Return DocumentChunk objects

==========================================================
"""

from models.document_chunk import DocumentChunk

from config.settings import MAX_PAGES_PER_CHUNK


class DocumentChunker:

    def __init__(
        self,
        max_pages_per_chunk=MAX_PAGES_PER_CHUNK
    ):

        self.max_pages = max_pages_per_chunk

    # ======================================================
    # Public
    # ======================================================

    def create_chunks(
        self,
        document
    ):

        chunks = []

        pages = document.pages

        chunk_id = 1

        for index in range(

            0,

            len(pages),

            self.max_pages

        ):

            chunk_pages = pages[

                index:index + self.max_pages

            ]

            text = "\n\n".join(

                page.text

                for page in chunk_pages

            )

            chunk = DocumentChunk(

                chunk_id=chunk_id,

                start_page=chunk_pages[0].page_number,

                end_page=chunk_pages[-1].page_number,

                text=text

            )

            chunks.append(chunk)

            chunk_id += 1

        return chunks