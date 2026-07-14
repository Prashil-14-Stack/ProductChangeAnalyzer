"""
==========================================================
Layout Element

Generic document layout object.

Every element detected in a document should eventually
be represented by this model.

Examples
--------
HEADING
PARAGRAPH
TABLE
FIGURE
LIST
HEADER
FOOTER

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class LayoutElement:

    # Identity
    element_id: int = 0

    page_number: int = 0

    # Classification
    element_type: str = "UNKNOWN"

    confidence: float = 0.0

    # Content
    text: str = ""

    # Geometry
    bbox: tuple = (0, 0, 0, 0)

    # Typography
    font_size: float = 0.0

    font_name: str = ""

    bold: bool = False

    italic: bool = False

    # Layout
    reading_order: int = 0

    column: int = 0

    # Metadata
    metadata: dict = field(default_factory=dict)

    @property
    def width(self):

        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):

        return self.bbox[3] - self.bbox[1]

    @property
    def area(self):

        return self.width * self.height