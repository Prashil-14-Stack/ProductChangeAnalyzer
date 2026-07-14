"""
==========================================================
Difference Result

Purpose
-------
Represents all structured differences between
two parameter values.

This object is populated by DifferenceEngine
and consumed by:

✓ ChangeAssessmentGenerator
✓ Excel Report
✓ Dashboard
✓ Future APIs

Contains NO comparison logic.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class DifferenceResult:

    # ======================================================
    # Original Values
    # ======================================================

    old_value: str = ""

    new_value: str = ""

    # ======================================================
    # Added / Removed Text
    # ======================================================

    added_text: list[str] = field(default_factory=list)

    removed_text: list[str] = field(default_factory=list)

    # ======================================================
    # Modified Sentences
    # ======================================================

    modified_sentences: list[dict] = field(default_factory=list)

    # Example
    #
    # [
    #   {
    #       "old": "...",
    #       "new": "..."
    #   }
    # ]

    # ======================================================
    # Numeric Changes
    # ======================================================

    number_changes: list[dict] = field(default_factory=list)

    # Example
    #
    # [
    #   {
    #       "old":"99",
    #       "new":"120"
    #   }
    # ]

    # ======================================================
    # Percentage Changes
    # ======================================================

    percentage_changes: list[dict] = field(default_factory=list)

    # ======================================================
    # Currency Changes
    # ======================================================

    currency_changes: list[dict] = field(default_factory=list)

    # ======================================================
    # Date Changes
    # ======================================================

    date_changes: list[dict] = field(default_factory=list)

    # ======================================================
    # Table Changes
    # ======================================================

    table_changes: list[dict] = field(default_factory=list)

    # ======================================================
    # Overall Summary
    # ======================================================

    summary: str = ""

    # ======================================================
    # Utility
    # ======================================================

    def has_changes(self):

        return any([

            self.added_text,

            self.removed_text,

            self.modified_sentences,

            self.number_changes,

            self.percentage_changes,

            self.currency_changes,

            self.date_changes,

            self.table_changes

        ])

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "old_value": self.old_value,

            "new_value": self.new_value,

            "added_text": self.added_text,

            "removed_text": self.removed_text,

            "modified_sentences": self.modified_sentences,

            "number_changes": self.number_changes,

            "percentage_changes": self.percentage_changes,

            "currency_changes": self.currency_changes,

            "date_changes": self.date_changes,

            "table_changes": self.table_changes,

            "summary": self.summary

        }