"""
==========================================================
Page Model

Purpose
-------
Represents a single page of a document.

A Page contains:

    • Page Number
    • Extracted Text
    • Optional Metadata

This model is independent of the document source
(PDF, DOCX, OCR, etc.).

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class Page:

    # ======================================================
    # Page Information
    # ======================================================

    page_number: int

    text: str = ""

    # ======================================================
    # Metadata
    # ======================================================

    metadata: dict = field(
        default_factory=dict
    )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def character_count(self):

        return len(self.text)

    # ------------------------------------------------------

    @property
    def word_count(self):

        return len(self.text.split())

    # ======================================================
    # Helpers
    # ======================================================

    def is_empty(self):

        return self.text.strip() == ""

    # ------------------------------------------------------

    def append_text(
        self,
        value: str
    ):

        if not value:

            return

        if self.text:

            self.text += "\n"

        self.text += value

    # ------------------------------------------------------

    def clear(self):

        self.text = ""

        self.metadata.clear()

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "page_number": self.page_number,

            "text": self.text,

            "character_count": self.character_count,

            "word_count": self.word_count,

            "metadata": self.metadata

        }

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):

        return (

            f"Page {self.page_number} | "

            f"{self.word_count} words"

        )