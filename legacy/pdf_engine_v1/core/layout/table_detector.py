"""
==========================================================
Enterprise Table Detector

Purpose
-------
Detect potential table regions from layout objects.

This detector DOES NOT extract table contents.

==========================================================
"""

from legacy.pdf_engine_v1.core.models.table_region import TableRegion


class TableDetector:

    TABLE_MIN_ROWS = 2

    ALIGNMENT_TOLERANCE = 8

    # ======================================================
    # Process
    # ======================================================

    def process(self, document):

        document.tables = []

        for page in document.pages:

            tables = self._detect_tables(page)

            document.tables.extend(tables)

        return document

    # ======================================================
    # Detect Tables
    # ======================================================

    def _detect_tables(self, page):

        tables = []

        current_table = None

        previous_y = None

        for block in page.layout_blocks:

            if self._looks_like_table_row(block):

                if current_table is None:

                    current_table = TableRegion(

                        page_number=page.page_number,

                        bbox=block.bbox,

                        confidence=0.7

                    )

                current_table.add_object(block)

                previous_y = block.bbox[1]

            else:

                if current_table:

                    if len(current_table.objects) >= self.TABLE_MIN_ROWS:

                        tables.append(current_table)

                    current_table = None

        if current_table:

            if len(current_table.objects) >= self.TABLE_MIN_ROWS:

                tables.append(current_table)

        return tables

    # ======================================================
    # Heuristic
    # ======================================================

    def _looks_like_table_row(self, block):

        text = block.text.strip()

        if not text:

            return False

        # Multiple large gaps usually indicate columns
        if "  " in text:

            return True

        # Numeric rows
        digits = sum(c.isdigit() for c in text)

        if digits >= 3:

            return True

        # Tab characters
        if "\t" in text:

            return True

        return False