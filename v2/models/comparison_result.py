"""
==========================================================
Comparison Result

Purpose
-------
Represents the final comparison output between two
ProductSpecifications.

Contains:

✓ Product Information
✓ All Comparison Items
✓ Summary Statistics

This object is consumed by:

✓ Excel Report Generator
✓ Word Report Generator
✓ JSON Export
✓ Future Dashboard

==========================================================
"""

from dataclasses import dataclass, field

from models.comparison_item import ComparisonItem


@dataclass
class ComparisonResult:

    # ======================================================
    # Product Information
    # ======================================================

    product_name_v1: str = ""

    product_name_v2: str = ""

    version_v1: str = ""

    version_v2: str = ""

    source_file_v1: str = ""

    source_file_v2: str = ""

    # ======================================================
    # Comparison Output
    # ======================================================

    items: list[ComparisonItem] = field(default_factory=list)

    summary: dict = field(default_factory=dict)

    # ======================================================
    # Helper Methods
    # ======================================================

    def add_item(self, item: ComparisonItem):

        self.items.append(item)

    # ------------------------------------------------------

    def total_items(self):

        return len(self.items)

    # ------------------------------------------------------

    def added_items(self):

        return [

            item

            for item in self.items

            if item.status == "Added"

        ]

    # ------------------------------------------------------

    def removed_items(self):

        return [

            item

            for item in self.items

            if item.status == "Removed"

        ]

    # ------------------------------------------------------

    def modified_items(self):

        return [

            item

            for item in self.items

            if item.status == "Modified"

        ]

    # ------------------------------------------------------

    def unchanged_items(self):

        return [

            item

            for item in self.items

            if item.status == "Unchanged"

        ]

    # ------------------------------------------------------

    def high_impact_items(self):

        return [

            item

            for item in self.items

            if item.impact == "High"

        ]

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "product_name_v1": self.product_name_v1,

            "product_name_v2": self.product_name_v2,

            "version_v1": self.version_v1,

            "version_v2": self.version_v2,

            "summary": self.summary,

            "items": [

                item.to_dict()

                for item in self.items

            ]

        }

    # ======================================================
    # Pretty Print
    # ======================================================

    def print_summary(self):

        print()

        print("=" * 80)

        print("COMPARISON RESULT")

        print("=" * 80)

        print(f"Product V1 : {self.product_name_v1}")

        print(f"Product V2 : {self.product_name_v2}")

        print()

        if self.summary:

            for key, value in self.summary.items():

                print(f"{key:20}: {value}")

        print()

        print(f"Comparison Items : {self.total_items()}")

        print("=" * 80)