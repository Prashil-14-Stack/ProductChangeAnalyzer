from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class BusinessChange:
    """
    Canonical representation of a detected business change
    between two versions of the same business parameter.
    """

    # ==========================================================
    # Business Parameter Objects (NEW)
    # ==========================================================

    source_parameter: Optional[Any] = None

    target_parameter: Optional[Any] = None

    # ==========================================================
    # Parameter Information (Backward Compatibility)
    # ==========================================================

    parameter: str = ""

    matched_parameter: Optional[str] = None

    # ==========================================================
    # Source Information
    # ==========================================================

    source_version: int = 0

    target_version: int = 0

    source_file: str = ""

    target_file: str = ""

    # ==========================================================
    # Original Content
    # ==========================================================

    old_text: str = ""

    new_text: str = ""

    # ==========================================================
    # Structured Change
    # ==========================================================

    change_type: str = ""

    difference_text: str = ""

    old_value: Optional[str] = None

    new_value: Optional[str] = None

    # ==========================================================
    # Added / Removed Content
    # ==========================================================

    added_text: List[str] = field(default_factory=list)

    removed_text: List[str] = field(default_factory=list)

    modified_segments: List[dict] = field(default_factory=list)

    # ==========================================================
    # AI Confidence
    # ==========================================================

    parameter_confidence: float = 0.0

    description_confidence: float = 0.0

    overall_confidence: float = 0.0

    # ==========================================================
    # Decision
    # ==========================================================

    decision: str = ""

    severity: str = ""

    # ==========================================================
    # Future Enterprise Features
    # ==========================================================

    nested_table_detected: bool = False

    requires_manual_review: bool = False

    metadata: dict = field(default_factory=dict)