"""
==========================================================
Figure Region

Represents one detected visual region.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class FigureRegion:

    page_number: int

    bbox: tuple

    figure_type: str = "UNKNOWN"

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)