"""
==========================================================
Table Cell

Represents a single logical cell within a detected table.

The cell is the smallest semantic unit of a table and
contains all information required for downstream
processing.

Used by

    • TableStructureBuilder
    • TableCellMerger
    • BusinessParameterExtractor
    • Comparator
    • AI Analyzer

==========================================================
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class TableCell:

    # ======================================================
    # Identity
    # ======================================================

    table_id: int = 0

    row_index: int = 0

    column_index: int = 0

    # ======================================================
    # Geometry
    # ======================================================

    bbox: Tuple[float, float, float, float] = (
        0.0,
        0.0,
        0.0,
        0.0
    )

    # ======================================================
    # Cell Content
    # ======================================================

    text: str = ""

    blocks: List = field(default_factory=list)

    # ======================================================
    # Span Information
    # ======================================================

    row_span: int = 1

    column_span: int = 1

    # ======================================================
    # Relationships
    # ======================================================

    parent_row: Optional[object] = None

    parent_table: Optional[object] = None

    # ======================================================
    # Formatting
    # ======================================================

    is_bold: bool = False

    font_size: float = 0.0

    alignment: str = "LEFT"

    # ======================================================
    # Confidence
    # ======================================================

    confidence: float = 1.0

    # ======================================================
    # Derived Properties
    # ======================================================

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

    @property
    def block_count(self):

        return len(self.blocks)

    # ======================================================
    # Operations
    # ======================================================

    def add_block(self, block):

        self.blocks.append(block)

        if not self.text:

            self.text = block.text

        else:

            self.text += "\n" + block.text

    # ------------------------------------------------------

    def merge(self, other):

        """
        Merge another cell into this one.

        Used for merged cells and wrapped content.
        """

        self.blocks.extend(other.blocks)

        self.text = " ".join(

            (self.text + " " + other.text).split()

        )

        self.row_span = max(

            self.row_span,

            other.row_span

        )

        self.column_span = max(

            self.column_span,

            other.column_span

        )

        x0 = min(self.bbox[0], other.bbox[0])
        y0 = min(self.bbox[1], other.bbox[1])
        x1 = max(self.bbox[2], other.bbox[2])
        y1 = max(self.bbox[3], other.bbox[3])

        self.bbox = (
            x0,
            y0,
            x1,
            y1
        )

    # ======================================================
    # Debug
    # ======================================================

    def summary(self):

        return (
            f"Row={self.row_index} | "
            f"Col={self.column_index} | "
            f"Span={self.row_span}x{self.column_span} | "
            f"Blocks={self.block_count} | "
            f"'{self.text[:60]}'"
        )

    # ======================================================
    # Representation
    # ======================================================

    def __str__(self):

        return (
            f"TableCell("
            f"r={self.row_index}, "
            f"c={self.column_index}, "
            f"text='{self.text[:40]}')"
        )

    __repr__ = __str__