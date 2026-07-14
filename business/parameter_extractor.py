"""
==========================================================
Business Parameter Extractor

Purpose
-------
Extract business parameters from the structured
document produced by the layout engine.

This extractor contains NO insurance knowledge.

All business knowledge comes from

    • insurance_dictionary.yaml
    • parameter_aliases.yaml

==========================================================
"""

from business.knowledge_loader import KnowledgeLoader
from models.business_parameter import BusinessParameter


class ParameterExtractor:

    def __init__(self):

        self.knowledge = KnowledgeLoader()

    # ======================================================
    # Process Document
    # ======================================================

    def process(self, document):

        document.business_parameters = []

        for section in document.sections:

            self._process_section(

                document,

                section

            )

        self._debug(document)

        return document

    # ======================================================
    # Section
    # ======================================================

    def _process_section(

        self,

        document,

        section

    ):

        # ------------------------------------------
        # Paragraphs
        # ------------------------------------------

        for paragraph in section.paragraphs:

            self._process_paragraph(

                document,

                paragraph,

                section

            )

        # ------------------------------------------
        # Tables
        # ------------------------------------------

        for table in section.tables:

            self._process_table(

                document,

                table,

                section

            )

    # ======================================================
    # Paragraph
    # ======================================================

    def _process_paragraph(

        self,

        document,

        paragraph,

        section

    ):

        text = paragraph.text.strip()

        if ":" not in text:

            return

        name, value = text.split(":", 1)

        name = name.strip()

        value = value.strip()

        if not self.knowledge.is_known_parameter(

            name

        ):

            return

        parameter = BusinessParameter(

            name=self.knowledge.normalize(name),

            value=value,

            category=self.knowledge.get_category(name),

            section=section.title,

            source="PARAGRAPH",

            page_number=paragraph.page_number,

            confidence=0.85,

            raw_text=text

        )

        document.business_parameters.append(

            parameter

        )

    # ======================================================
    # Tables
    # ======================================================

    def _process_table(

        self,

        document,

        table,

        section

    ):

        for row in table.rows:

            if len(row.cells) < 2:

                continue

            parameter_name = row.cells[0].text.strip()

            parameter_value = row.cells[1].text.strip()

            if not self.knowledge.is_known_parameter(

                parameter_name

            ):

                continue

            parameter = BusinessParameter(

                name=self.knowledge.normalize(

                    parameter_name

                ),

                value=parameter_value,

                category=self.knowledge.get_category(

                    parameter_name

                ),

                section=section.title,

                source="TABLE",

                page_number=table.page_number,

                table_id=table.table_id,

                row_index=row.row_index,

                column_index=0,

                confidence=0.95,

                raw_text=parameter_name

            )

            document.business_parameters.append(

                parameter

            )

    # ======================================================
    # Debug
    # ======================================================

    def _debug(

        self,

        document

    ):

        print()

        print("=" * 100)

        print("BUSINESS PARAMETERS")

        print("=" * 100)

        if not document.business_parameters:

            print("No business parameters detected.")

            return

        for parameter in document.business_parameters:

            print()

            print(parameter.name)

            print(f"Value      : {parameter.value}")

            print(f"Category   : {parameter.category}")

            print(f"Section    : {parameter.section}")

            print(f"Source     : {parameter.source}")

            print(f"Confidence : {parameter.confidence:.2f}")