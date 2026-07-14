"""
==========================================================
Comparison Sheet

Purpose
-------
Creates the flagship Product Comparison worksheet.

This worksheet closely resembles the DOCX-era comparison
report while leveraging the AI comparison engine.

Responsibilities
----------------
✓ Product Comparison
✓ Confidence Metrics
✓ Difference Summary
✓ Business Assessment
✓ Professional Formatting

==========================================================
"""

from v2.reports.formatting import ExcelFormatter


class ComparisonSheet:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.formatter = ExcelFormatter()

    # ======================================================
    # Public
    # ======================================================

    def build(
        self,
        workbook,
        comparison_result
    ):

        ws = workbook.create_sheet("Parameter Comparison")

        # ==================================================
        # Report Title
        # ==================================================

        ws.merge_cells("A1:W1")

        ws["A1"] = "PRODUCT CHANGE ANALYSIS REPORT"

        self.formatter.apply_title(ws["A1"])

        # ==================================================
        # Column Headers
        # ==================================================

        headers = [

            "Source Version",
            "Target Version",
            "V1 Parameter",
            "Matched V2 Parameter",
            "Parameter Confidence (%)",
            "Confidence Band",
            "Description Confidence (%)",
            "Overall Confidence (%)",
            "Decision",
            "Status",
            "V1 Content",
            "V2 Content",
            "Difference",
            "Change Type",
            "Severity",
            "Remarks",
            "Summary",
            "Business Impact",
            "Affected Teams",
            "Testing",
            "Risk",
            "Priority",
            "Business Criticality"

        ]

        HEADER_ROW = 2

        for col, header in enumerate(headers, start=1):

            cell = ws.cell(
                row=HEADER_ROW,
                column=col
            )

            cell.value = header

            self.formatter.apply_header(cell)

        # ==================================================
        # Data Rows
        # ==================================================

        row = HEADER_ROW + 1

        for item in comparison_result.items:

            # ----------------------------------------------
            # Confidence Calculations
            # ----------------------------------------------

            parameter_confidence = round(
                max(
                    item.confidence_v1,
                    item.confidence_v2
                ) * 100,
                2
            )

            # Placeholder until semantic similarity engine
            description_confidence = parameter_confidence

            overall_confidence = round(
                (
                    parameter_confidence +
                    description_confidence
                ) / 2,
                2
            )

            if overall_confidence >= 90:

                confidence_band = "High"

            elif overall_confidence >= 70:

                confidence_band = "Medium"

            else:

                confidence_band = "Low"

            decision = item.status

            values = [

                getattr(
                    comparison_result,
                    "version_v1",
                    comparison_result.product_name_v1
                ),

                getattr(
                    comparison_result,
                    "version_v2",
                    comparison_result.product_name_v2
                ),

                item.parameter_name,

                getattr(
                    item,
                    "matched_parameter",
                    item.parameter_name
                ),

                parameter_confidence,

                confidence_band,

                description_confidence,

                overall_confidence,

                decision,

                item.status,

                item.old_value,

                item.new_value,

                getattr(
                    item,
                    "difference_summary",
                    ""
                ),

                getattr(
                    item,
                    "change_type",
                    item.status
                ),

                item.impact,

                getattr(
                    item,
                    "remarks",
                    ""
                ),

                getattr(
                    item,
                    "summary",
                    ""
                ),

                getattr(
                    item,
                    "business_impact",
                    ""
                ),

                getattr(
                    item,
                    "affected_teams",
                    ""
                ),

                getattr(
                    item,
                    "testing_recommendation",
                    ""
                ),

                getattr(
                    item,
                    "risk",
                    ""
                ),

                getattr(
                    item,
                    "priority",
                    ""
                ),

                getattr(
                    item,
                    "business_criticality",
                    ""
                )

            ]

            for col, value in enumerate(values, start=1):

                cell = ws.cell(
                    row=row,
                    column=col
                )

                cell.value = value

                self.formatter.apply_body(cell)

                cell.alignment = self.formatter.wrap_alignment()

            # ----------------------------------------------
            # Colour Coding
            # ----------------------------------------------

            self.formatter.apply_status_colour(
                ws.cell(row=row, column=10),
                item.status
            )

            self.formatter.apply_impact_colour(
                ws.cell(row=row, column=15),
                item.impact
            )

            row += 1

        # ==================================================
        # Formatting
        # ==================================================

        #self.formatter.freeze_header(
         #   ws,
         #  HEADER_ROW + 1
        #)

        self.formatter.apply_filter(
            ws,
            HEADER_ROW
        )

        #self.formatter.autofit_columns(ws)

        #self.formatter.apply_default_row_heights(ws)

        return ws