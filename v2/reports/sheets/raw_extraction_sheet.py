"""
==========================================================
Raw Extraction Sheet

Purpose
-------
Displays the raw BusinessParameters extracted
from the Product Specification.

This worksheet provides traceability between
the original document and the comparison engine.

Responsibilities
----------------
✓ Show extracted parameters
✓ Show extracted values
✓ Show categories
✓ Show sections
✓ Show page numbers
✓ Show confidence

==========================================================
"""

from v2.reports.formatting import ExcelFormatter


class RawExtractionSheet:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(
        self,
        sheet_name="Raw Extraction"
    ):

        self.sheet_name = sheet_name

        self.formatter = ExcelFormatter()

    # ======================================================
    # Build
    # ======================================================

    def build(
        self,
        workbook,
        specification
    ):

        ws = workbook.create_sheet(
            self.sheet_name
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        ws.merge_cells("A1:F1")

        ws["A1"] = self.sheet_name.upper()

        self.formatter.apply_title(
            ws["A1"]
        )

        # --------------------------------------------------
        # Product Information
        # --------------------------------------------------

        row = 3

        info = [

            ("Product Name", specification.product_name),

            ("Version", specification.product_version),

            ("Insurer", specification.insurer),

            ("Document Type", specification.document_type)

        ]

        for label, value in info:

            ws[f"A{row}"] = label

            ws[f"B{row}"] = "" if value is None else str(value)

            self.formatter.apply_sub_header(
                ws[f"A{row}"]
            )

            self.formatter.apply_body(
                ws[f"B{row}"]
            )

            row += 1

        row += 2

        # --------------------------------------------------
        # Table Header
        # --------------------------------------------------

        headers = [

            "Parameter",

            "Value",

            "Category",

            "Section",

            "Page",

            "Confidence"

        ]

        for col, header in enumerate(headers, start=1):

            cell = ws.cell(
                row=row,
                column=col
            )

            cell.value = header

            self.formatter.apply_header(
                cell
            )

        row += 1

        # --------------------------------------------------
        # Parameters
        # --------------------------------------------------

        for parameter in specification.parameters:

            values = [

                parameter.name,

                parameter.value,

                parameter.category,

                parameter.section,

                parameter.page_number,

                parameter.confidence

            ]

            for col, value in enumerate(values, start=1):

                cell = ws.cell(
                    row=row,
                    column=col
                )

                cell.value = "" if value is None else str(value)

                self.formatter.apply_body(
                    cell
                )

            row += 1

        # --------------------------------------------------
        # Freeze Header
        # --------------------------------------------------

        self.formatter.freeze_header(
            ws,
            row=8
        )

        # --------------------------------------------------
        # Filter
        # --------------------------------------------------

        self.formatter.apply_filter(
            ws
        )

        # --------------------------------------------------
        # Formatting
        # --------------------------------------------------

        self.formatter.autofit_columns(
            ws
        )

        self.formatter.apply_default_row_heights(
            ws
        )