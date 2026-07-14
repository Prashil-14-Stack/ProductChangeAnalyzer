"""
==========================================================
JSON Report Generator

Purpose
-------
Exports ComparisonResult to a structured JSON file.

Responsibilities
----------------
✓ Export comparison result
✓ Pretty-print JSON
✓ Create output folder if needed

==========================================================
"""

import json
from pathlib import Path


class JSONReportGenerator:

    """
    Generates JSON reports from ComparisonResult.
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, output_folder="output"):

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
        filename="comparison_report.json"
    ):

        output_path = self.output_folder / filename

        report = {

            "product_v1": {

                "name": comparison_result.product_name_v1,

                "version": comparison_result.version_v1,

                "source_file": comparison_result.source_file_v1

            },

            "product_v2": {

                "name": comparison_result.product_name_v2,

                "version": comparison_result.version_v2,

                "source_file": comparison_result.source_file_v2

            },

            "summary": comparison_result.summary,

            "comparison_items": [

                item.to_dict()

                for item in comparison_result.items

            ]

        }

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        return output_path

    # ======================================================
    # Utility
    # ======================================================

    def print_location(
        self,
        output_path
    ):

        print()

        print("=" * 80)

        print("JSON REPORT GENERATED")

        print("=" * 80)

        print(output_path)

        print("=" * 80)