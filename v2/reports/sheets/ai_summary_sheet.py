"""
==========================================================
AI Insights Sheet

Purpose
-------
Displays structured AI insights for business,
testing and implementation teams.

Responsibilities
----------------
✓ Overall Risk
✓ Team Impact
✓ Testing Impact
✓ Compliance Impact
✓ Product Configuration Impact
✓ Deployment Readiness

==========================================================
"""

from v2.reports.formatting import ExcelFormatter


class AISummarySheet:

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
        business_summary=None
    ):

        ws = workbook.create_sheet(
            "AI Insights"
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        ws.merge_cells("A1:F1")

        ws["A1"] = "AI BUSINESS INSIGHTS"

        self.formatter.apply_title(
            ws["A1"]
        )

        row = 3

        # --------------------------------------------------
        # Overall Summary
        # --------------------------------------------------

        ws[f"A{row}"] = "Overall AI Summary"

        self.formatter.apply_sub_header(
            ws[f"A{row}"]
        )

        row += 1

        ws.merge_cells(
            start_row=row,
            start_column=1,
            end_row=row + 10,
            end_column=6
        )

        cell = ws.cell(
            row=row,
            column=1
        )

        if business_summary:

            cell.value = self._escape_excel(
                business_summary
            )

        else:

            cell.value = "AI Summary not available."

        self.formatter.apply_body(cell)

        row += 13

        # --------------------------------------------------
        # Implementation Checklist
        # --------------------------------------------------

        ws[f"A{row}"] = "Suggested Review Checklist"

        self.formatter.apply_sub_header(
            ws[f"A{row}"]
        )

        row += 1

        checklist = [

            ("Product Team", "Review configuration changes"),

            ("Business Analyst", "Validate requirement differences"),

            ("QA / UAT", "Prepare regression test cases"),

            ("Compliance", "Review regulatory impact"),

            ("Actuarial", "Validate pricing / benefit changes"),

            ("Operations", "Review servicing impact")

        ]

        for team, action in checklist:

            ws[f"A{row}"] = team

            ws[f"B{row}"] = action

            self.formatter.apply_body(
                ws[f"A{row}"]
            )

            self.formatter.apply_body(
                ws[f"B{row}"]
            )

            row += 1

        row += 1

        # --------------------------------------------------
        # Deployment Guidance
        # --------------------------------------------------

        ws[f"A{row}"] = "Deployment Guidance"

        self.formatter.apply_sub_header(
            ws[f"A{row}"]
        )

        row += 1

        guidance = [

            "Review all High Impact Changes before deployment.",

            "Complete UAT for modified business parameters.",

            "Validate product configuration with Product Team.",

            "Obtain Compliance approval before release.",

            "Confirm actuarial sign-off where benefits changed."

        ]

        for item in guidance:

            ws[f"A{row}"] = "•"

            ws[f"B{row}"] = item

            self.formatter.apply_body(
                ws[f"A{row}"]
            )

            self.formatter.apply_body(
                ws[f"B{row}"]
            )

            row += 1

        # --------------------------------------------------
        # Formatting
        # --------------------------------------------------

        self.formatter.autofit_columns(ws)

        self.formatter.apply_default_row_heights(ws)

    def _escape_excel(self, text):

        if text is None:
            return ""

        text = str(text)

        if text.startswith("="):
            text = "'" + text

        return text