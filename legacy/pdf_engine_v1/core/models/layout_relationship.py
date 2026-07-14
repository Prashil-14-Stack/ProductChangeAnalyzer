"""
==========================================================
Layout Relationship

Represents a relationship (edge) between two LayoutObjects.

This forms the foundation of the Layout Graph.

Example

Heading
    ↓ contains
Paragraph

Table Header
    ↓ same_row
Table Cell

Paragraph
    ↓ below
Paragraph

==========================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ==========================================================
# Relationship Types
# ==========================================================

class RelationshipType(Enum):

    # Reading Order
    PREVIOUS = "PREVIOUS"
    NEXT = "NEXT"

    # Spatial
    LEFT_OF = "LEFT_OF"
    RIGHT_OF = "RIGHT_OF"
    ABOVE = "ABOVE"
    BELOW = "BELOW"

    # Alignment
    SAME_ROW = "SAME_ROW"
    SAME_COLUMN = "SAME_COLUMN"

    LEFT_ALIGNED = "LEFT_ALIGNED"
    RIGHT_ALIGNED = "RIGHT_ALIGNED"
    CENTER_ALIGNED = "CENTER_ALIGNED"

    # Containment
    CONTAINS = "CONTAINS"
    CHILD_OF = "CHILD_OF"

    # Document Structure
    BELONGS_TO_SECTION = "BELONGS_TO_SECTION"
    BELONGS_TO_TABLE = "BELONGS_TO_TABLE"
    BELONGS_TO_LIST = "BELONGS_TO_LIST"

    # Continuation
    CONTINUES = "CONTINUES"

    # Generic
    RELATED = "RELATED"


# ==========================================================
# Layout Relationship
# ==========================================================

@dataclass
class LayoutRelationship:
    """
    Graph edge connecting two LayoutObjects.
    """

    # ------------------------------------------------------
    # Graph Nodes
    # ------------------------------------------------------

    source: Optional[Any] = None

    target: Optional[Any] = None

    # ------------------------------------------------------
    # Relationship
    # ------------------------------------------------------

    relationship_type: RelationshipType = RelationshipType.RELATED

    confidence: float = 1.0

    # ------------------------------------------------------
    # Optional Metrics
    # ------------------------------------------------------

    distance: float = 0.0

    overlap_x: float = 0.0

    overlap_y: float = 0.0

    metadata: dict = field(default_factory=dict)

    # ======================================================
    # Helper Properties
    # ======================================================

    @property
    def source_text(self):

        if self.source is None:
            return ""

        return getattr(self.source, "text", "")

    @property
    def target_text(self):

        if self.target is None:
            return ""

        return getattr(self.target, "text", "")

    # ======================================================
    # Representation
    # ======================================================

    def __str__(self):

        source = self.source_text[:40].replace("\n", " ")

        target = self.target_text[:40].replace("\n", " ")

        return (
            f"{source} "
            f"--[{self.relationship_type.value}]--> "
            f"{target} "
            f"(confidence={self.confidence:.2f})"
        )

    __repr__ = __str__