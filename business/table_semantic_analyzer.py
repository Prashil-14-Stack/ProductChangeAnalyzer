"""
==========================================================
Table Semantic Analyzer

Purpose
-------
Analyze reconstructed tables and determine their business
meaning.

Responsibilities

✓ Detect header row
✓ Identify column roles
✓ Detect table type
✓ Annotate tables for downstream extraction

No AI
No LLM
Deterministic rules only

==========================================================
"""

import re


class TableSemanticAnalyzer:

    # ------------------------------------------------------
    # Known Header Keywords
    # ------------------------------------------------------

    PARAMETER_HEADERS = {

        "parameter",
        "feature",
        "attribute",
        "criteria",
        "benefit",
        "description"
    }

    VALUE_HEADERS = {

        "value",
        "details",
        "description",
        "information"
    }

    VARIANT_HEADERS = {

        "variant",
        "plan",
        "option",
        "product"
    }

    # ======================================================
    # Process
    # ======================================================

    def process(self, document):

        tables = getattr(document, "tables", [])

        for table in tables:

            self._analyze(table)

        self._debug(document)

        return document

    # ======================================================
    # Analyze One Table
    # ======================================================

    def _analyze(self, table):

        table.semantic_type = "UNKNOWN"

        table.parameter_column = None

        table.value_column = None

        table.header_row = None

        if not table.rows:

            return

        header = table.rows[0]

        table.header_row = header

        for cell in header.cells:

            text = cell.text.strip().lower()

            if self._contains(text, self.PARAMETER_HEADERS):

                table.parameter_column = cell.column_index

            if self._contains(text, self.VALUE_HEADERS):

                table.value_column = cell.column_index

        # ------------------------------------------
        # Determine Table Type
        # ------------------------------------------

        header_text = " ".join(

            cell.text.lower()

            for cell in header.cells

        )

        if self._contains(

            header_text,

            self.VARIANT_HEADERS

        ):

            table.semantic_type = "VARIANT_COMPARISON"

        elif (

            table.parameter_column is not None

            and

            table.value_column is not None

        ):

            table.semantic_type = "PARAMETER_VALUE"

        else:

            table.semantic_type = "GENERIC"

    # ======================================================
    # Helper
    # ======================================================

    def _contains(

        self,

        text,

        keywords

    ):

        for keyword in keywords:

            if re.search(

                rf"\b{re.escape(keyword)}\b",

                text

            ):

                return True

        return False

    # ======================================================
    # Debug
    # ======================================================

    def _debug(self, document):

        print()

        print("=" * 100)

        print("TABLE SEMANTIC ANALYZER")

        print("=" * 100)

        tables = getattr(document, "tables", [])

        if not tables:

            print("No tables found.")
            return

        for table in tables:

            print()

            print(f"Table ID          : {table.table_id}")

            print(f"Type              : {table.semantic_type}")

            print(f"Header Row        : {0 if table.header_row else None}")

            print(f"Parameter Column  : {table.parameter_column}")

            print(f"Value Column      : {table.value_column}")

            print()

            if table.header_row:

                print("Headers")

                for cell in table.header_row.cells:

                    print(

                        f"  [{cell.column_index}] {cell.text}"

                    )