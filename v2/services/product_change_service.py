"""
==========================================================
Product Change Service

Purpose
-------
Enterprise orchestration layer for the complete
Product Change Analyzer workflow.

Responsibilities
----------------
✓ Read documents
✓ Extract business parameters
✓ Compare products
✓ Generate AI business summary
✓ Generate reports

This class contains NO business logic.

==========================================================
"""

from pathlib import Path
import tempfile
import pandas as pd

from v2.readers.reader_factory import ReaderFactory

from v2.llm.llm_service import LLMService

from v2.comparison.comparison_engine import ComparisonEngine

from v2.ai.business_summary_generator import BusinessSummaryGenerator

from v2.reports.excel_report_generator import ExcelReportGenerator


class ProductChangeService:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.reader_factory = ReaderFactory()

        self.llm_service = LLMService()

        self.comparison_engine = ComparisonEngine()

        self.summary_generator = BusinessSummaryGenerator()

        self.report_generator = ExcelReportGenerator()

    # ======================================================
    # Public API
    # ======================================================

    def compare_products(

        self,

        version1_file,

        version2_file

    ):

        # --------------------------------------------------
        # Read Documents
        # --------------------------------------------------

        document_v1 = self._read_document(

            version1_file

        )

        document_v2 = self._read_document(

            version2_file

        )

        # --------------------------------------------------
        # Extract Specifications
        # --------------------------------------------------

        specification_v1 = self.llm_service.extract_product_specification(

            document_v1

        )

        specification_v2 = self.llm_service.extract_product_specification(

            document_v2

        )

        specification_v1.product_version = Path(
            version1_file.name
        ).stem

        specification_v2.product_version = Path(
            version2_file.name
        ).stem
        # --------------------------------------------------
        # Compare
        # --------------------------------------------------

        comparison_result = self.comparison_engine.compare(

            specification_v1,

            specification_v2

        )

        # --------------------------------------------------
        # AI Business Summary
        # --------------------------------------------------

        business_summary = self.summary_generator.generate(

            comparison_result

        )
        print("=" * 80)
        print("BUSINESS SUMMARY")
        print("=" * 80)
        print(repr(business_summary[:300]))

        # --------------------------------------------------
        # Excel Report
        # --------------------------------------------------

        report_path = self.report_generator.generate(

            comparison_result,

            specification_v1,

            specification_v2,

            business_summary

        )


        # --------------------------------------------------
        # Build Comparison DataFrame for Streamlit
        # --------------------------------------------------

        comparison_table = pd.DataFrame(

            [

                {

                    "Business Parameter": item.parameter_name,

                    "Status": item.status,

                    "Impact": item.impact,

                    "Category": item.category,

                    "Section": item.section,

                    "Old Value": item.old_value,

                    "New Value": item.new_value,

                    "Reason": item.reason

                }

                for item in comparison_result.items

            ]

        )

        # --------------------------------------------------
        # Calculate Metrics
        # --------------------------------------------------

        added = sum(
            1 for item in comparison_result.items
            if item.status == "Added"
        )

        removed = sum(
            1 for item in comparison_result.items
            if item.status == "Removed"
        )

        modified = sum(
            1 for item in comparison_result.items
            if item.status == "Modified"
        )

        unchanged = sum(
            1 for item in comparison_result.items
            if item.status == "Unchanged"
        )

        metrics = {

            # Dashboard
            "parameters": len(comparison_result.items),

            "matches": unchanged,

            "changes": added + removed + modified,

            "repository": 2,

            # Detailed Statistics
            "added": added,

            "removed": removed,

            "modified": modified,

            "unchanged": unchanged,

            # Impact
            "high_impact": sum(
                1
                for item in comparison_result.items
                if item.impact == "High"
            ),

            "medium_impact": sum(
                1
                for item in comparison_result.items
                if item.impact == "Medium"
            ),

            "low_impact": sum(
                1
                for item in comparison_result.items
                if item.impact == "Low"
            )

        }

        # --------------------------------------------------
        # Return to Streamlit
        # --------------------------------------------------

        return {

            "documents": [

                {

                    "version": "Version 1",

                    "filename": version1_file.name

                },

                {

                    "version": "Version 2",

                    "filename": version2_file.name

                }

            ],

            "comparisons": [

                {

                    "source": {

                        "version": 1,

                        "filename": version1_file.name

                    },

                    "target": {

                        "version": 2,

                        "filename": version2_file.name

                    }

                }

            ],

            "comparison_table": comparison_table,

            "metrics": metrics,

            "report_path": str(report_path),

            "comparison_result": comparison_result,

            "business_summary": business_summary,

            "specification_v1": specification_v1,

            "specification_v2": specification_v2

        }

    # ======================================================
    # Helpers
    # ======================================================

    def _read_document(
        self,
        uploaded_file
    ):

            # --------------------------------------------------
            # Save Streamlit UploadedFile as a temporary file
            # --------------------------------------------------

            suffix = Path(uploaded_file.name).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())

                temp_path = temp_file.name

            # --------------------------------------------------
            # Read document using existing readers
            # --------------------------------------------------

            reader = self.reader_factory.get_reader(
                temp_path
            )

            return reader.read(
                temp_path
            )