"""
==========================================================
Table Region

Represents one complete table detected within a document.

Hierarchy

TableRegion
    ├── TableRow
    │       ├── TableCell
    │       ├── TableCell
    │       └── ...
    │
    ├── TableRow
    └── ...

==========================================================
"""

from dataclasses import dataclass, field
from typing import List

from legacy.pdf_engine_v1.core.models.table_row import TableRow


@dataclass
class TableRegion:
    """
    Represents one logical table.
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    table_id: int = -1

    page_number: int = 0

    # --------------------------------------------------
    # Rows
    # --------------------------------------------------

    rows: List[TableRow] = field(default_factory=list)

    # --------------------------------------------------
    # Geometry
    # --------------------------------------------------

    bbox: tuple = (0, 0, 0, 0)

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    confidence: float = 0.0

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict = field(default_factory=dict)

    # ==================================================
    # Add Row
    # ==================================================

    def add_row(self, row: TableRow):

        row.table_id = self.table_id

        self.rows.append(row)

        self._update_bbox()

    # ==================================================
    # Bounding Box
    # ==================================================

    def _update_bbox(self):

        if not self.rows:
            return

        x0 = min(row.bbox[0] for row in self.rows)
        y0 = min(row.bbox[1] for row in self.rows)
        x1 = max(row.bbox[2] for row in self.rows)
        y1 = max(row.bbox[3] for row in self.rows)

        self.bbox = (
            x0,
            y0,
            x1,
            y1
        )

    # ==================================================
    # Convenience Properties
    # ==================================================

    @property
    def row_count(self):

        return len(self.rows)

    @property
    def column_count(self):

        if not self.rows:
            return 0

        return max(

            len(row.cells)

            for row in self.rows

        )

    @property
    def cell_count(self):

        return sum(

            len(row.cells)

            for row in self.rows

        )

    @property
    def header(self):

        if not self.rows:
            return None

        return self.rows[0]

    @property
    def data_rows(self):

        if len(self.rows) <= 1:
            return []

        return self.rows[1:]

    @property
    def text(self):

        return "\n".join(

            row.text

            for row in self.rows

        )

    @property
    def width(self):

        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):

        return self.bbox[3] - self.bbox[1]

    # ==================================================
    # Sort Rows
    # ==================================================

    def sort_rows(self):

        self.rows.sort(

            key=lambda r: r.row_index

        )

        for row in self.rows:

            row.sort_cells()

    # ==================================================
    # Get Cell
    # ==================================================

    def get_cell(

        self,

        row_index,

        column_index

    ):

        if row_index >= len(self.rows):

            return None

        row = self.rows[row_index]

        if column_index >= len(row.cells):

            return None

        return row.cells[column_index]

    # ==================================================
    # String Representation
    # ==================================================

    def __str__(self):

        return (

            f"TableRegion("

            f"id={self.table_id}, "

            f"rows={self.row_count}, "

            f"columns={self.column_count}, "

            f"cells={self.cell_count})"

        )

    __repr__ = __str__