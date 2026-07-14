"""
==========================================================
Excel Report Generator

Purpose
-------
Master orchestrator for generating the complete
Product Comparison Excel Report.

Responsibilities
----------------
✓ Create workbook
✓ Invoke each worksheet generator
✓ Save workbook

This class contains NO worksheet logic.

==========================================================
"""

from pathlib import Path

from openpyxl import Workbook

from v2.reports.sheets.dashboard_sheet import DashboardSheet
from v2.reports.sheets.executive_summary_sheet import ExecutiveSummarySheet
from v2.reports.sheets.comparison_sheet import ComparisonSheet
from v2.reports.sheets.high_impact_sheet import HighImpactSheet
from v2.reports.sheets.added_sheet import AddedSheet
from v2.reports.sheets.removed_sheet import RemovedSheet
from v2.reports.sheets.raw_extraction_sheet import RawExtractionSheet
from v2.reports.sheets.ai_summary_sheet import AISummarySheet
from v2.reports.sheets.metrics_sheet import MetricsSheet


class ExcelReportGenerator:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(
        self,
        output_folder="output"
    ):

        self.output_folder = Path(output_folder)

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # Public
    # ======================================================

    def generate(

        self,

        comparison_result,

        specification_v1,

        specification_v2,

        business_summary=None,

        filename="Product_Comparison_Report.xlsx"

    ):

        workbook = Workbook()

        # Remove default worksheet

        workbook.remove(
            workbook.active
        )

        # ==============================================
        # Dashboard
        # ==============================================

        DashboardSheet().build(

            workbook,

            comparison_result

        )

        # ==============================================
        # Executive Summary
        # ==============================================

        ExecutiveSummarySheet().build(

            workbook,

            comparison_result,

            business_summary

        )

        # ==============================================
        # Detailed Comparison
        # ==============================================

        ComparisonSheet().build(

            workbook,

            comparison_result

        )

        # ==============================================
        # High Impact Changes
        # ==============================================

        HighImpactSheet().build(

            workbook,

            comparison_result

        )

        # ==============================================
        # Added Parameters
        # ==============================================

        AddedSheet().build(

            workbook,

            comparison_result

        )

        # ==============================================
        # Removed Parameters
        # ==============================================

        RemovedSheet().build(

            workbook,

            comparison_result

        )

        # ==============================================
        # Raw Extraction Version 1
        # ==============================================

        RawExtractionSheet(

            "Raw Extraction V1"

        ).build(

            workbook,

            specification_v1

        )

        # ==============================================
        # Raw Extraction Version 2
        # ==============================================

        RawExtractionSheet(

            "Raw Extraction V2"

        ).build(

            workbook,

            specification_v2

        )

        # ==============================================
        # AI Summary
        # ==============================================

        AISummarySheet().build(

            workbook,

            business_summary

        )

        # ==============================================
        # Metrics & Charts
        # ==============================================

        MetricsSheet().build(

            workbook,

            comparison_result

        )

        # ==============================================
        # Save Workbook
        # ==============================================

        output_path = self.output_folder / filename

        workbook.save(output_path)

        return output_path