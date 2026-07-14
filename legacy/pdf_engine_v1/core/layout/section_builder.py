"""
==========================================================
Enterprise Section Builder

Purpose
-------
Construct a hierarchical document from headings.

Input
-----
Layout Blocks
Heading Detector
Tables
Figures
Lists

Output
------
Document Sections

Document

    Section

        Paragraphs

        Tables

        Figures

        Lists

        Child Sections

==========================================================
"""

from legacy.pdf_engine_v1.core.models.document_section import DocumentSection


class SectionBuilder:

    def process(self, document):

        document.sections = []

        current_section = None

        for page in document.pages:

            for block in page.layout_blocks:

                # --------------------------------------
                # New Heading
                # --------------------------------------

                if getattr(block, "is_heading", False):

                    section = DocumentSection(

                        title=block.text.strip(),

                        page_number=page.page_number,

                        heading_level=getattr(
                            block,
                            "heading_level",
                            1
                        ),

                        bbox=block.bbox

                    )

                    document.sections.append(section)

                    current_section = section

                    continue

                # --------------------------------------
                # Ignore until first heading
                # --------------------------------------

                if current_section is None:

                    continue

                # --------------------------------------
                # Paragraph
                # --------------------------------------

                block_type = getattr(

                    block,

                    "block_type",

                    "UNKNOWN"

                )

                if block_type == "PARAGRAPH":

                    current_section.add_paragraph(block)

                    continue

                # --------------------------------------
                # List
                # --------------------------------------

                if block_type == "LIST":

                    current_section.add_list(block)

                    continue

                # --------------------------------------
                # Figure
                # --------------------------------------

                if block_type == "FIGURE":

                    current_section.add_figure(block)

                    continue

                # --------------------------------------
                # Table
                # --------------------------------------

                if hasattr(block, "table_id"):

                    table = self._find_table(

                        document,

                        block.table_id

                    )

                    if table:

                        current_section.add_table(table)

        self._build_hierarchy(document)

        self._debug(document)

        return document

    # ======================================================
    # Table Lookup
    # ======================================================

    def _find_table(

        self,

        document,

        table_id

    ):

        for table in document.tables:

            if table.table_id == table_id:

                return table

        return None

    # ======================================================
    # Build Parent / Child Hierarchy
    # ======================================================

    def _build_hierarchy(

        self,

        document

    ):

        stack = []

        for section in document.sections:

            while (

                stack

                and

                stack[-1].heading_level

                >=

                section.heading_level

            ):

                stack.pop()

            if stack:

                parent = stack[-1]

                section.parent = parent

                parent.children.append(section)

            stack.append(section)

    # ======================================================
    # Debug
    # ======================================================

    def _debug(

        self,

        document

    ):

        print()

        print("=" * 100)

        print("DOCUMENT SECTIONS")

        print("=" * 100)

        for section in document.sections:

            indent = "    " * (

                section.heading_level - 1

            )

            print()

            print(

                f"{indent}H{section.heading_level}: "

                f"{section.title}"

            )

            print(

                f"{indent}Paragraphs : "

                f"{len(section.paragraphs)}"

            )

            print(

                f"{indent}Tables     : "

                f"{len(section.tables)}"

            )

            print(

                f"{indent}Figures    : "

                f"{len(section.figures)}"

            )

            print(

                f"{indent}Lists      : "

                f"{len(section.lists)}"

            )