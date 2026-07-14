"""
==========================================================
Table Cell Merger

Purpose
-------
Merge wrapped text belonging to the same table cell.

Example

Income Benefit
after deferment
period

↓

Income Benefit after deferment period

The TableDetector identifies the table.

The TableStructureBuilder identifies the cells.

This module cleans the cell contents.

==========================================================
"""


class TableCellMerger:

    def process(self, document):

        tables = getattr(document, "tables", [])

        for table in tables:

            self._process_table(table)

        return document

    # ------------------------------------------------------

    def _process_table(self, table):

        rows = getattr(table, "rows", [])

        for row in rows:

            cells = getattr(row, "cells", [])

            for cell in cells:

                self._merge_cell(cell)

    # ------------------------------------------------------

    def _merge_cell(self, cell):

        blocks = getattr(cell, "blocks", [])

        if not blocks:

            return

        merged_lines = []

        for block in blocks:

            text = block.text.strip()

            if not text:

                continue

            lines = [

                line.strip()

                for line in text.splitlines()

                if line.strip()

            ]

            merged_lines.extend(lines)

        # ---------------------------------------------
        # Merge wrapped lines
        # ---------------------------------------------

        merged_text = " ".join(merged_lines)

        # Remove duplicated spaces

        merged_text = " ".join(

            merged_text.split()

        )

        cell.text = merged_text

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------

    def debug(self, document):

        print("\n")
        print("=" * 100)
        print("TABLE CELL MERGER")
        print("=" * 100)

        tables = getattr(document, "tables", [])

        if not tables:

            print("No tables detected.")
            return

        for table in tables:

            print()

            print(f"Table {table.table_id}")

            rows = getattr(table, "rows", [])

            for row_index, row in enumerate(rows, 1):

                print()

                print(f"Row {row_index}")

                cells = getattr(row, "cells", [])

                for col_index, cell in enumerate(cells, 1):

                    print(

                        f"  Cell {col_index}: {cell.text}"

                    )