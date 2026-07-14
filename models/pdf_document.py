from dataclasses import dataclass, field
from typing import List, Dict

from models.pdf_page import PDFPage


@dataclass
class PDFDocument:
    """
    ==========================================================
    Enterprise PDF Document

    Canonical representation of an entire PDF document.

    This object is the root of the PDF layout hierarchy.

    PDFDocument
        │
        ├── PDFPage
        │       ├── LayoutBlock
        │       │       ├── LayoutLine
        │       │       │       └── LayoutSpan
        │       │
        │       ├── Images
        │       └── Tables
        │
        └── Metadata

    No business logic should exist here.
    This object only represents the document.

    ==========================================================
    """

    # ==========================================================
    # Basic Information
    # ==========================================================

    filename: str

    file_path: str = ""

    source_type: str = "PDF"

    version: int = 1

    # ==========================================================
    # Content
    # ==========================================================

    pages: List[PDFPage] = field(default_factory=list)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Processing
    # ==========================================================

    processing_status: str = "RAW"

    # ==========================================================
    # Add Page
    # ==========================================================

    def add_page(

        self,

        page: PDFPage

    ):

        self.pages.append(page)

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def page_count(self):

        return len(self.pages)

    @property
    def total_blocks(self):

        return sum(

            page.block_count

            for page in self.pages

        )

    @property
    def total_tables(self):

        return sum(

            page.table_count

            for page in self.pages

        )

    @property
    def total_images(self):

        return sum(

            page.image_count

            for page in self.pages

        )

    @property
    def text(self):
        """
        Returns the complete document text.
        """

        return "\n\n".join(

            page.text

            for page in self.pages

            if page.text.strip()

        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self):

        return {

            "filename": self.filename,

            "source_type": self.source_type,

            "version": self.version,

            "page_count": self.page_count,

            "blocks": self.total_blocks,

            "tables": self.total_tables,

            "images": self.total_images,

            "status": self.processing_status

        }

    # ==========================================================
    # String Representation
    # ==========================================================

    def __str__(self):

        return (

            f"PDFDocument("

            f"filename='{self.filename}', "

            f"pages={self.page_count}, "

            f"blocks={self.total_blocks}, "

            f"tables={self.total_tables}, "

            f"images={self.total_images}"

            f")"

        )