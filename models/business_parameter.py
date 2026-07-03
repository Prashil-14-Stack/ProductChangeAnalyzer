from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class BusinessParameter:
    """
    Represents a business parameter extracted from an
    insurance product specification.
    """

    # ======================================================
    # Identity
    # ======================================================

    name: str

    normalized_name: str

    category: str = "General"

    # ======================================================
    # Content
    # ======================================================

    value: str = ""

    raw_text: str = ""

    # ======================================================
    # Document Traceability
    # ======================================================

    page_number: int = 0

    block_number: int = 0

    table_number: int = 0

    source_document: str = ""

    # ======================================================
    # Extraction Metadata
    # ======================================================

    confidence: float = 100.0

    extraction_method: str = "Rule Based"

    # ======================================================
    # NLP Metadata
    # ======================================================

    tokens: List[str] = field(default_factory=list)

    business_terms: List[str] = field(default_factory=list)

    detected_values: List[str] = field(default_factory=list)

    # ======================================================
    # Business Metadata
    # ======================================================

    business_critical: bool = False

    requires_review: bool = False

    affected_modules: List[str] = field(default_factory=list)

    # ======================================================
    # Future Extensions
    # ======================================================

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Convenience Properties
    # ======================================================

    @property
    def has_value(self) -> bool:

        return bool(self.value.strip())

    @property
    def token_count(self) -> int:

        return len(self.tokens)

    @property
    def business_term_count(self) -> int:

        return len(self.business_terms)

    # ======================================================
    # Utility
    # ======================================================

    def summary(self):

        return {

            "name": self.name,

            "category": self.category,

            "value": self.value,

            "page": self.page_number,

            "confidence": self.confidence

        }