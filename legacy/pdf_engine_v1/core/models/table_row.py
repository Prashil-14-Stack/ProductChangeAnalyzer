"""
==========================================================
Table Row

Represents one logical row inside a detected table.

A row consists of one or more TableCell objects.

==========================================================
"""

from dataclasses import dataclass, field
from typing import List

from legacy.pdf_engine_v1.core.models.table_cell import TableCell


@dataclass
class TableRow:
    """
    Represents a single row within a table.
    """

    # --------------------------------------------------
    # Row Information
    # --------------------------------------------------

    row_index: int = -1

    page_number: int = 0

    table_id: int | None = None

    # --------------------------------------------------
    # Cells
    # --------------------------------------------------

    cells: List[TableCell] = field(default_factory=list)

    # --------------------------------------------------
    # Geometry
    # --------------------------------------------------

    bbox: tuple = (0, 0, 0, 0)

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    is_header: bool = False

    confidence: float = 0.0

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict = field(default_factory=dict)

    # ==================================================
    # Add Cell
    # ==================================================

    def add_cell(self, cell: TableCell):

        cell.row_index = self.row_index

        cell.table_id = self.table_id

        self.cells.append(cell)

        self._update_bbox()

    # ==================================================
    # Update Bounding Box
    # ==================================================

    def _update_bbox(self):

        if not self.cells:
            return

        x0 = min(cell.bbox[0] for cell in self.cells)
        y0 = min(cell.bbox[1] for cell in self.cells)
        x1 = max(cell.bbox[2] for cell in self.cells)
        y1 = max(cell.bbox[3] for cell in self.cells)

        self.bbox = (x0, y0, x1, y1)

    # ==================================================
    # Convenience Properties
    # ==================================================

    @property
    def cell_count(self):

        return len(self.cells)

    @property
    def text(self):

        return " | ".join(

            cell.text.strip()

            for cell in self.cells

        )

    @property
    def width(self):

        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):

        return self.bbox[3] - self.bbox[1]

    # ==================================================
    # Sort Cells
    # ==================================================

    def sort_cells(self):

        self.cells.sort(

            key=lambda c: c.column_index

        )

    # ==================================================
    # Representation
    # ==================================================

    def __str__(self):

        return (

            f"TableRow("

            f"row={self.row_index}, "

            f"cells={self.cell_count}, "

            f"text='{self.text[:60]}')"

        )

    __repr__ = __str__