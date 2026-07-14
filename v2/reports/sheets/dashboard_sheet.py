"""
==========================================================
Dashboard Sheet

Purpose
-------
Creates the executive dashboard.

This is the first worksheet in the report.

Responsibilities
----------------
✓ Product Information
✓ KPI Summary
✓ High Impact Changes
✓ Recommended Review Teams

==========================================================
"""

from v2.reports.formatting import ExcelFormatter


class DashboardSheet:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.formatter = ExcelFormatter()

    # ======================================================
    # Build Sheet
    # ======================================================

    def build(
        self,
        workbook,
        comparison_result
    ):

        ws = workbook.create_sheet(
            "Dashboard"
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        ws.merge_cells("A1:F1")

        ws["A1"] = "PRODUCT CHANGE ANALYZER"

        self.formatter.apply_title(ws["A1"])

        # --------------------------------------------------
        # Report Information
        # --------------------------------------------------

        row = 3

        info = [

            ("Product Version 1", comparison_result.product_name_v1),

            ("Product Version 2", comparison_result.product_name_v2),

            ("Version 1", comparison_result.version_v1),

            ("Version 2", comparison_result.version_v2)

        ]

        for label, value in info:

            ws[f"A{row}"] = label

            ws[f"B{row}"] = value

            self.formatter.apply_sub_header(
                ws[f"A{row}"]
            )

            self.formatter.apply_body(
                ws[f"B{row}"]
            )

            row += 1

        row += 2

        # --------------------------------------------------
        # KPI Summary
        # --------------------------------------------------

        ws[f"A{row}"] = "Comparison Summary"

        self.formatter.apply_sub_header(
            ws[f"A{row}"]
        )

        row += 1

        summary = comparison_result.summary

        kpis = [

            ("Total Parameters",
             summary.get("total_parameters", 0)),

            ("Modified",
             summary.get("modified", 0)),

            ("Added",
             summary.get("added", 0)),

            ("Removed",
             summary.get("removed", 0)),

            ("Unchanged",
             summary.get("unchanged", 0)),

            ("High Impact",
             summary.get("high_impact", 0)),

            ("Medium Impact",
             summary.get("medium_impact", 0)),

            ("Low Impact",
             summary.get("low_impact", 0))

        ]

        for label, value in kpis:

            ws[f"A{row}"] = label

            ws[f"B{row}"] = value

            self.formatter.apply_body(
                ws[f"A{row}"]
            )

            self.formatter.apply_body(
                ws[f"B{row}"]
            )

            row += 1

        row += 2

        # --------------------------------------------------
        # High Impact Parameters
        # --------------------------------------------------

        ws[f"A{row}"] = "High Impact Changes"

        self.formatter.apply_sub_header(
            ws[f"A{row}"]
        )

        row += 1

        high_impact = [

            item

            for item in comparison_result.items

            if item.impact.lower() == "high"

        ]

        if high_impact:

            for item in high_impact:

                ws[f"A{row}"] = item.parameter_name

                ws[f"B{row}"] = item.status

                ws[f"C{row}"] = item.impact

                self.formatter.apply_body(
                    ws[f"A{row}"]
                )

                self.formatter.apply_status_colour(
                    ws[f"B{row}"],
                    item.status
                )

                self.formatter.apply_impact_colour(
                    ws[f"C{row}"],
                    item.impact
                )

                row += 1

        else:

            ws[f"A{row}"] = "No High Impact Changes"

            self.formatter.apply_body(
                ws[f"A{row}"]
            )

            row += 1

        row += 2

        # --------------------------------------------------
        # Recommended Review Teams
        # --------------------------------------------------

        ws[f"A{row}"] = "Recommended Review Teams"

        self.formatter.apply_sub_header(
            ws[f"A{row}"]
        )

        row += 1

        teams = [

            "Product Team",

            "Business Analysis",

            "QA / UAT",

            "Compliance",

            "Actuarial"

        ]

        for team in teams:

            ws[f"A{row}"] = "✔"

            ws[f"B{row}"] = team

            self.formatter.apply_body(
                ws[f"A{row}"]
            )

            self.formatter.apply_body(
                ws[f"B{row}"]
            )

            row += 1

        # --------------------------------------------------
        # Freeze
        # --------------------------------------------------

        self.formatter.freeze_header(
            ws,
            row=3
        )
        self.formatter.autofit_columns(
            ws
        )

        self.formatter.apply_default_row_heights(
            ws
        )