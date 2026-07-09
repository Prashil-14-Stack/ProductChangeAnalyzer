"""
==========================================================
Business Parameter Model

Purpose
-------
Represents one business parameter extracted from a
product specification.

This model is source-independent.

The parameter may originate from:

    • PDF
    • DOCX
    • JSON
    • Manual Entry

==========================================================
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BusinessParameter:

    # ======================================================
    # Identity
    # ======================================================

    name: str

    value: str

    # ======================================================
    # Classification
    # ======================================================

    category: str = ""

    # ======================================================
    # Source Information
    # ======================================================

    source: str = ""

    page_number: Optional[int] = None

    section: str = ""

    # ======================================================
    # AI Metadata
    # ======================================================

    confidence: float = 1.0

    reasoning: str = ""

    # ======================================================
    # Comparison
    # ======================================================

    comparison_status: str = ""

    previous_value: str = ""

    current_value: str = ""

    # ======================================================
    # Traceability
    # ======================================================

    raw_text: str = ""

    # ======================================================
    # Additional Metadata
    # ======================================================

    metadata: dict = field(default_factory=dict)

    # ======================================================
    # Helpers
    # ======================================================

    def has_changed(self) -> bool:

        return (

            self.previous_value != ""

            and

            self.current_value != ""

            and

            self.previous_value != self.current_value

        )

    # ------------------------------------------------------

    def is_empty(self) -> bool:

        return (

            self.name.strip() == ""

            and

            self.value.strip() == ""

        )

    # ------------------------------------------------------

    def to_dict(self):

        return {

            "name": self.name,

            "value": self.value,

            "category": self.category,

            "source": self.source,

            "page_number": self.page_number,

            "section": self.section,

            "confidence": self.confidence,

            "reasoning": self.reasoning,

            "comparison_status": self.comparison_status,

            "previous_value": self.previous_value,

            "current_value": self.current_value,

            "raw_text": self.raw_text,

            "metadata": self.metadata

        }

    # ------------------------------------------------------

    def __str__(self):

        return (

            f"{self.name} = {self.value}"

        )