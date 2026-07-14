"""
==========================================================
Document Model

Purpose
-------
Represents a complete document within
ProductChangeAnalyzer V2.

A Document contains:

    • File Information
    • Pages
    • Extracted Text
    • Metadata

The Document model is intentionally independent of
PDF, DOCX, or any future file format.

==========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from v2.models.page import Page


@dataclass
class Document:

    # ======================================================
    # File Information
    # ======================================================

    file_name: str = ""

    file_path: str = ""

    file_type: str = ""

    file_size: int = 0

    # ======================================================
    # Document Content
    # ======================================================

    pages: List[Page] = field(
        default_factory=list
    )

    # ======================================================
    # Metadata
    # ======================================================

    metadata: dict = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )

    # ======================================================
    # Page Operations
    # ======================================================

    def add_page(
        self,
        page: Page
    ):

        self.pages.append(page)

    # ------------------------------------------------------

    def page_count(self):

        return len(self.pages)

    # ------------------------------------------------------

    def get_page(
        self,
        page_number: int
    ):

        for page in self.pages:

            if page.page_number == page_number:

                return page

        return None

    # ======================================================
    # Text Operations
    # ======================================================

    @property
    def text(self):

        """
        Returns the complete document text.
        """

        return "\n\n".join(

            page.text

            for page in self.pages

        )

    # ------------------------------------------------------

    def word_count(self):

        return sum(

            page.word_count

            for page in self.pages

        )

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "file_name": self.file_name,

            "file_path": self.file_path,

            "file_type": self.file_type,

            "file_size": self.file_size,

            "page_count": self.page_count(),

            "word_count": self.word_count(),

            "metadata": self.metadata,

            "pages": [

                page.to_dict()

                for page in self.pages

            ]

        }

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        return {

            "File": self.file_name,

            "Type": self.file_type,

            "Pages": self.page_count(),

            "Words": self.word_count()

        }

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):

        return (

            f"{self.file_name} "

            f"({self.page_count()} pages)"

        )