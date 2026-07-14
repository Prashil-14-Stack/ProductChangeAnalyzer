"""
==========================================================
Enterprise Table Structure Builder (Phase 1)

Purpose
-------
Discover the logical table grid.

This phase performs

✓ Row Detection
✓ Column Detection
✓ Grid Construction

This phase DOES NOT

✗ Create TableCell
✗ Merge Cells
✗ Detect Headers

==========================================================
"""

from collections import defaultdict


class TableStructureBuilder:

    ROW_TOLERANCE = 8

    COLUMN_TOLERANCE = 15

    # =====================================================
    # Process
    # =====================================================

    def process(self, document):

        document.detected_grids = []

        for page in document.pages:

            grid = self._build_grid(page)

            if grid:

                document.detected_grids.append(grid)

        self._debug(document)

        return document

    # =====================================================
    # Build Grid
    # =====================================================

    def _build_grid(self, page):

        blocks = getattr(page, "layout_blocks", [])

        if not blocks:

            return None

        rows = self._detect_rows(blocks)

        columns = self._detect_columns(blocks)

        grid = {

            "page": page.page_number,

            "rows": rows,

            "columns": columns

        }

        return grid

    # =====================================================
    # Detect Rows
    # =====================================================

    def _detect_rows(self, blocks):

        buckets = defaultdict(list)

        for block in blocks:

            y = block.bbox[1]

            bucket = round(

                y / self.ROW_TOLERANCE

            )

            buckets[bucket].append(block)

        rows = []

        for bucket in sorted(buckets.keys()):

            row_blocks = sorted(

                buckets[bucket],

                key=lambda b: b.bbox[0]

            )

            rows.append(row_blocks)

        return rows

    # =====================================================
    # Detect Columns
    # =====================================================

    def _detect_columns(self, blocks):

        x_positions = []

        for block in blocks:

            x = block.bbox[0]

            found = False

            for existing in x_positions:

                if abs(existing - x) <= self.COLUMN_TOLERANCE:

                    found = True

                    break

            if not found:

                x_positions.append(x)

        x_positions.sort()

        return x_positions

    # =====================================================
    # Debug
    # =====================================================

    def _debug(self, document):

        print()

        print("=" * 100)

        print("GRID DETECTOR")

        print("=" * 100)

        grids = getattr(

            document,

            "detected_grids",

            []

        )

        if not grids:

            print("No grids detected.")

            return

        for grid in grids:

            print()

            print(f"Page : {grid['page']}")

            print()

            print(

                f"Rows Detected    : {len(grid['rows'])}"

            )

            print(

                f"Columns Detected : {len(grid['columns'])}"

            )

            print()

            print("Column Positions")

            for index, x in enumerate(grid["columns"]):

                print(

                    f"Column {index:<2} -> {x:.2f}"

                )

            print()

            print("Rows")

            for index, row in enumerate(grid["rows"]):

                print()

                print(f"Row {index}")

                for block in row:

                    print(

                        f"   ({block.bbox[0]:.1f}) "

                        f"{block.text[:60]}"

                    )