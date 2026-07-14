"""
==========================================================
Removed Parameters Sheet

Purpose
-------
Lists all business parameters removed from
Version 2.

Responsibilities
----------------
✓ Display Removed Parameters
✓ Highlight retired business rules

==========================================================
"""

from v2.reports.formatting import ExcelFormatter


class RemovedSheet:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.formatter = ExcelFormatter()

    # ======================================================
    # Build
    # ======================================================

    def build(
        self,
        workbook,
        comparison_result
    ):

        ws = workbook.create_sheet(
            "Removed Parameters"
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        ws.merge_cells("A1:F1")

        ws["A1"] = "REMOVED BUSINESS PARAMETERS"

        self.formatter.apply_title(
            ws["A1"]
        )

        # --------------------------------------------------
        # Headers
        # --------------------------------------------------

        headers = [

            "Business Parameter",

            "Impact",

            "Category",

            "Section",

            "Old Value",

            "Reason"

        ]

        row = 3

        for col, header in enumerate(headers, start=1):

            cell = ws.cell(
                row=row,
                column=col
            )

            cell.value = header

            self.formatter.apply_header(
                cell
            )

        # --------------------------------------------------
        # Removed Parameters
        # --------------------------------------------------

        row += 1

        count = 0

        for item in comparison_result.items:

            if item.status.lower() != "removed":

                continue

            values = [

                item.parameter_name,

                item.impact,

                item.category,

                item.section,

                item.old_value,

                item.reason

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

            # ------------------------------------------
            # Highlight Impact
            # ------------------------------------------

            self.formatter.apply_impact_colour(

                ws.cell(
                    row=row,
                    column=2
                ),

                item.impact

            )

            row += 1

            count += 1

        # --------------------------------------------------
        # No Removed Parameters
        # --------------------------------------------------

        if count == 0:

            ws.merge_cells(
                start_row=4,
                start_column=1,
                end_row=4,
                end_column=6
            )

            cell = ws["A4"]

            cell.value = "No Business Parameters Removed"

            self.formatter.apply_body(
                cell
            )

        # --------------------------------------------------
        # Freeze Header
        # --------------------------------------------------

        self.formatter.freeze_header(
            ws,
            row=4
        )

        # --------------------------------------------------
        # Filter
        # --------------------------------------------------

        self.formatter.apply_filter(
            ws
        )

        # --------------------------------------------------
        # Auto Fit
        # --------------------------------------------------

        self.formatter.autofit_columns(
            ws
        )

        self.formatter.apply_default_row_heights(
            ws
        )