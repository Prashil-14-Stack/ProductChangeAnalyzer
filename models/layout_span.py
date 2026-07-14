from dataclasses import dataclass, field
from typing import Dict


@dataclass
class LayoutSpan:
    """
    ==========================================================
    Enterprise PDF Layout Span

    Smallest unit extracted from a PDF.

    A span typically represents text sharing the same
    font, size, styling and position.

    Example

        "Plan Description"

    or

        "18 Years"

    ==========================================================
    """

    # ==========================================================
    # Content
    # ==========================================================

    text: str

    # ==========================================================
    # Position
    # ==========================================================

    bbox: tuple

    origin: tuple

    # ==========================================================
    # Font Information
    # ==========================================================

    font: str

    font_size: float

    flags: int

    color: int

    # ==========================================================
    # Optional Metadata
    # ==========================================================

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def is_bold(self):

        """
        PyMuPDF flag bit 4 usually indicates bold.
        """

        return bool(self.flags & 16)

    @property
    def is_italic(self):

        """
        PyMuPDF flag bit 1 usually indicates italic.
        """

        return bool(self.flags & 2)

    @property
    def width(self):

        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):

        return self.bbox[3] - self.bbox[1]

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self):

        return {

            "text": self.text,

            "font": self.font,

            "font_size": self.font_size,

            "bold": self.is_bold,

            "italic": self.is_italic,

            "bbox": self.bbox

        }

    # ==========================================================
    # String Representation
    # ==========================================================

    def __str__(self):

        return (

            f"LayoutSpan("

            f"text='{self.text}', "

            f"font='{self.font}', "

            f"size={self.font_size}"

            f")"

        )