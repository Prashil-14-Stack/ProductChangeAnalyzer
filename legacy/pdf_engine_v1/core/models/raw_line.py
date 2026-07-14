"""
==========================================================
Raw Line

Represents one physical line extracted from a PDF.

Hierarchy

RawDocument
    └── RawBlock
            └── RawLine
                    └── RawSpan

No document intelligence is applied here.

==========================================================
"""

from dataclasses import dataclass, field
from typing import List, Tuple

from legacy.pdf_engine_v1.core.models.raw_span import RawSpan


@dataclass
class RawLine:
    """
    Represents one physical text line.
    """

    # ------------------------------------------------------
    # Geometry
    # ------------------------------------------------------

    bbox: Tuple[float, float, float, float] = (
        0.0,
        0.0,
        0.0,
        0.0
    )

    # ------------------------------------------------------
    # Spans
    # ------------------------------------------------------

    spans: List[RawSpan] = field(default_factory=list)

    # ------------------------------------------------------
    # Add Span
    # ------------------------------------------------------

    def add_span(self, span: RawSpan):

        self.spans.append(span)

        self._update_bbox()

    # ------------------------------------------------------
    # Bounding Box
    # ------------------------------------------------------

    def _update_bbox(self):

        if not self.spans:
            return

        x0 = min(span.bbox[0] for span in self.spans)
        y0 = min(span.bbox[1] for span in self.spans)
        x1 = max(span.bbox[2] for span in self.spans)
        y1 = max(span.bbox[3] for span in self.spans)

        self.bbox = (
            x0,
            y0,
            x1,
            y1
        )

    # ------------------------------------------------------
    # Text
    # ------------------------------------------------------

    @property
    def text(self):

        return "".join(

            span.text

            for span in self.spans

        ).strip()

    # ------------------------------------------------------
    # Typography
    # ------------------------------------------------------

    @property
    def average_font_size(self):

        if not self.spans:
            return 0

        return sum(

            span.font_size

            for span in self.spans

        ) / len(self.spans)

    @property
    def dominant_font(self):

        if not self.spans:
            return ""

        fonts = {}

        for span in self.spans:

            fonts[span.font] = fonts.get(span.font, 0) + 1

        return max(

            fonts,

            key=fonts.get

        )

    @property
    def is_bold(self):

        if not self.spans:
            return False

        return any(

            span.is_bold

            for span in self.spans

        )

    @property
    def is_italic(self):

        if not self.spans:
            return False

        return any(

            span.is_italic

            for span in self.spans

        )

    # ------------------------------------------------------
    # Geometry Helpers
    # ------------------------------------------------------

    @property
    def width(self):

        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):

        return self.bbox[3] - self.bbox[1]

    @property
    def center_x(self):

        return (self.bbox[0] + self.bbox[2]) / 2

    @property
    def center_y(self):

        return (self.bbox[1] + self.bbox[3]) / 2

    @property
    def span_count(self):

        return len(self.spans)

    @property
    def is_empty(self):

        return self.text == ""

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------

    def summary(self):

        return (
            f"{self.text} | "
            f"Spans={self.span_count} | "
            f"Font={self.dominant_font} | "
            f"Size={self.average_font_size:.1f}"
        )

    # ------------------------------------------------------
    # Representation
    # ------------------------------------------------------

    def __str__(self):

        return (
            f"RawLine("
            f"spans={self.span_count}, "
            f"text='{self.text[:60]}')"
        )

    __repr__ = __str__