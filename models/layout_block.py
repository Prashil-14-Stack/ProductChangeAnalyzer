from dataclasses import dataclass, field
from typing import List, Dict

from models.layout_line import LayoutLine


@dataclass
class LayoutBlock:
    """
    ==========================================================
    Enterprise PDF Layout Block

    Represents one logical block extracted from a PDF page.

    A block consists of one or more LayoutLine objects.

    Typical examples:

        • Heading
        • Paragraph
        • Table
        • Bullet List
        • Footer
        • Image Caption

    This is the primary object that will be classified
    by the Layout Classification Engine.

    ==========================================================
    """

    # ==========================================================
    # Identification
    # ==========================================================

    block_number: int

    page_number: int

    # ==========================================================
    # Content
    # ==========================================================

    lines: List[LayoutLine] = field(default_factory=list)

    # ==========================================================
    # Position
    # ==========================================================

    bbox: tuple = (0, 0, 0, 0)

    # ==========================================================
    # Classification
    # ==========================================================

    block_type: str = "UNKNOWN"

    classification_confidence: float = 0.0

    classification_reasons: List[str] = field(default_factory=list)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Add Line
    # ==========================================================

    def add_line(

        self,

        line: LayoutLine

    ):

        self.lines.append(

            line

        )

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def text(self):

        """
        Returns the complete block text.
        """

        return "\n".join(

            line.text

            for line in self.lines

            if line.text.strip()

        )

    @property
    def line_count(self):

        return len(

            self.lines

        )

    @property
    def span_count(self):

        return sum(

            line.span_count

            for line in self.lines

        )

    @property
    def average_font_size(self):

        if not self.lines:

            return 0

        sizes = [

            line.average_font_size

            for line in self.lines

            if line.average_font_size > 0

        ]

        if not sizes:

            return 0

        return round(

            sum(sizes) / len(sizes),

            2

        )

    @property
    def has_bold_text(self):

        return any(

            line.has_bold_text

            for line in self.lines

        )

    @property
    def has_italic_text(self):

        return any(

            line.has_italic_text

            for line in self.lines

        )

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

            "page": self.page_number,

            "block": self.block_number,

            "type": self.block_type,

            "lines": self.line_count,

            "spans": self.span_count,

            "font_size": self.average_font_size,

            "bold": self.has_bold_text,

            "italic": self.has_italic_text,

            "bbox": self.bbox

        }

    # ==========================================================
    # String Representation
    # ==========================================================

    def __str__(self):

        return (

            f"LayoutBlock("

            f"page={self.page_number}, "

            f"block={self.block_number}, "

            f"type='{self.block_type}', "

            f"lines={self.line_count}"

            f")"

        )