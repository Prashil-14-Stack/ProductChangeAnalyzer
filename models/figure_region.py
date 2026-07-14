"""
==========================================================
Figure Region

Represents a non-text visual object detected
within a document.

Examples
--------
- Company Logo
- Flow Diagram
- Chart
- Product Illustration
- SmartArt
- Watermark

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