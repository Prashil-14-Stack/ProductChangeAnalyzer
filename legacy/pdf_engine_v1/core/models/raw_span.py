"""
==========================================================
Raw Span

Represents the smallest text element extracted from PyMuPDF.

Hierarchy

RawDocument
    └── RawBlock
            └── RawLine
                    └── RawSpan

No interpretation is performed here.

==========================================================
"""

from dataclasses import dataclass, field
from typing import Tuple, List


@dataclass
class RawSpan:
    """
    Smallest text fragment extracted from the PDF.
    """

    # ------------------------------------------------------
    # Text
    # ------------------------------------------------------

    text: str = ""

    # ------------------------------------------------------
    # Geometry
    # ------------------------------------------------------

    bbox: Tuple[float, float, float, float] = (
        0.0,
        0.0,
        0.0,
        0.0
    )

    origin: Tuple[float, float] = (
        0.0,
        0.0
    )

    # ------------------------------------------------------
    # Typography
    # ------------------------------------------------------

    font: str = ""

    font_size: float = 0.0

    flags: int = 0

    color: int = 0

    # ------------------------------------------------------
    # Characters
    # ------------------------------------------------------

    characters: List[str] = field(default_factory=list)

    # ------------------------------------------------------
    # Derived Properties
    # ------------------------------------------------------

    @property
    def character_count(self):

        if self.characters:
            return len(self.characters)

        return len(self.text)

    @property
    def is_bold(self):

        return (
            "bold" in self.font.lower()
            or self.flags & 16 != 0
        )

    @property
    def is_italic(self):

        return (
            "italic" in self.font.lower()
            or self.flags & 2 != 0
        )

    @property
    def width(self):

        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):

        return self.bbox[3] - self.bbox[1]

    @property
    def center_x(self):

        return (self.bbox[0] + self.bbox[2]) / 2

    @property
    def center_y(self):

        return (self.bbox[1] + self.bbox[3]) / 2

    @property
    def is_empty(self):

        return self.text.strip() == ""

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------

    def summary(self):

        return (
            f"'{self.text}' | "
            f"{self.font} | "
            f"{self.font_size:.1f} pt | "
            f"Bold={self.is_bold}"
        )

    # ------------------------------------------------------
    # Representation
    # ------------------------------------------------------

    def __str__(self):

        return (
            f"RawSpan("
            f"text='{self.text[:40]}', "
            f"font='{self.font}', "
            f"size={self.font_size:.1f})"
        )

    __repr__ = __str__