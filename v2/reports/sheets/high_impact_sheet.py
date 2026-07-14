"""
==========================================================
High Impact Changes Sheet

Purpose
-------
Lists only HIGH impact product changes.

Responsibilities
----------------
✓ Filter High Impact Changes
✓ Display comparison details
✓ Highlight critical changes

==========================================================
"""

from v2.reports.formatting import ExcelFormatter


class HighImpactSheet:

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
            "High Impact Changes"
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        ws.merge_cells("A1:G1")

        ws["A1"] = "HIGH IMPACT PRODUCT CHANGES"

        self.formatter.apply_title(
            ws["A1"]
        )

        # --------------------------------------------------
        # Headers
        # --------------------------------------------------

        headers = [

            "Business Parameter",

            "Status",

            "Impact",

            "Category",

            "Old Value",

            "New Value",

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
        # Filter High Impact Changes
        # --------------------------------------------------

        row += 1

        count = 0

        for item in comparison_result.items:

            if item.impact.lower() != "high":

                continue

            values = [

                item.parameter_name,

                item.status,

                item.impact,

                item.category,

                item.old_value,

                item.new_value,

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

            # ----------------------------------------------
            # Status Colour
            # ----------------------------------------------

            self.formatter.apply_status_colour(

                ws.cell(
                    row=row,
                    column=2
                ),

                item.status

            )

            # ----------------------------------------------
            # Impact Colour
            # ----------------------------------------------

            self.formatter.apply_impact_colour(

                ws.cell(
                    row=row,
                    column=3
                ),

                item.impact

            )

            row += 1

            count += 1

        # --------------------------------------------------
        # No High Impact Changes
        # --------------------------------------------------

        if count == 0:

            ws.merge_cells(
                start_row=4,
                start_column=1,
                end_row=4,
                end_column=7
            )

            cell = ws["A4"]

            cell.value = "No High Impact Changes Identified"

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