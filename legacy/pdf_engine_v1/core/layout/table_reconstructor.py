"""
==========================================================
Table Reconstructor

Purpose
-------
Reconstruct logical tables from fragmented cells.

Responsibilities

✓ Merge vertically split cells
✓ Merge wrapped header cells
✓ Remove duplicate fragments
✓ Preserve traceability

This module NEVER creates new tables.

It only improves existing TableRegion objects.

==========================================================
"""

from copy import deepcopy


class TableReconstructor:

    # Maximum vertical distance between fragments
    VERTICAL_GAP = 12

    # Maximum horizontal difference for same column
    COLUMN_TOLERANCE = 15

    def process(self, document):

        tables = getattr(document, "tables", [])

        for table in tables:

            self._reconstruct(table)

        self._debug(document)

        return document

    # ======================================================
    # Reconstruct One Table
    # ======================================================

    def _reconstruct(self, table):

        self._merge_vertical(table)

        self._merge_horizontal(table)

        self._remove_empty(table)

        table.sort_rows()

    # ======================================================
    # Merge Vertical Fragments
    # ======================================================

    def _merge_vertical(self, table):

        for row_index in range(len(table.rows) - 1):

            current = table.rows[row_index]

            below = table.rows[row_index + 1]

            for cell in current.cells:

                partner = self._find_same_column(

                    below,

                    cell.column_index

                )

                if partner is None:

                    continue

                if self._should_merge(

                    cell,

                    partner

                ):

                    cell.text = (

                        cell.text.rstrip()

                        + " "

                        + partner.text.lstrip()

                    ).strip()

                    cell.bbox = (

                        min(cell.bbox[0], partner.bbox[0]),

                        min(cell.bbox[1], partner.bbox[1]),

                        max(cell.bbox[2], partner.bbox[2]),

                        max(cell.bbox[3], partner.bbox[3])

                    )

                    partner.text = ""

    # ======================================================
    # Merge Wrapped Headers
    # ======================================================

    def _merge_horizontal(self, table):

        if not table.rows:

            return

        header = table.rows[0]

        for i in range(len(header.cells) - 1):

            left = header.cells[i]

            right = header.cells[i + 1]

            # Skip if either is empty
            if not left.text.strip() or not right.text.strip():
                continue

            # Merge if both are very short words and likely wrapped
            if (
                len(left.text.split()) <= 2
                and len(right.text.split()) <= 2
            ):

                gap = right.bbox[0] - left.bbox[2]

                if gap < self.COLUMN_TOLERANCE:

                    left.text = (

                        left.text.rstrip()

                        + " "

                        + right.text.lstrip()

                    ).strip()

                    right.text = ""

    # ======================================================
    # Helpers
    # ======================================================

    def _find_same_column(

        self,

        row,

        column_index

    ):

        for cell in row.cells:

            if cell.column_index == column_index:

                return cell

        return None

    # ======================================================

    def _should_merge(

        self,

        top,

        bottom

    ):

        if not top.text.strip():

            return False

        if not bottom.text.strip():

            return False

        gap = bottom.bbox[1] - top.bbox[3]

        return gap <= self.VERTICAL_GAP

    # ======================================================
    # Remove Empty Cells
    # ======================================================

    def _remove_empty(self, table):

        for row in table.rows:

            row.cells = [

                cell

                for cell in row.cells

                if cell.text.strip()

            ]

    # ======================================================
    # Debug
    # ======================================================

    def _debug(self, document):

        print()

        print("=" * 100)
        print("TABLE RECONSTRUCTOR")
        print("=" * 100)

        tables = getattr(document, "tables", [])

        if not tables:

            print("No tables available.")
            return

        for table in tables:

            print()

            print(f"Table {table.table_id}")

            print(f"Rows    : {table.row_count}")

            print(f"Columns : {table.column_count}")

            print()

            for row in table.rows:

                values = []

                for cell in row.cells:

                    values.append(cell.text)

                print(" | ".join(values))