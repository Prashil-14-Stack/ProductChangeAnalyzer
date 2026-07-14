from dataclasses import dataclass, field
from typing import List, Dict

from models.layout_span import LayoutSpan


@dataclass
class LayoutLine:
    """
    ==========================================================
    Enterprise PDF Layout Line

    Represents one visual line inside a PDF block.

    A line consists of one or more LayoutSpan objects.

    Example

        Plan Description

    may consist of multiple spans having different
    fonts or formatting.

    ==========================================================
    """

    # ==========================================================
    # Content
    # ==========================================================

    spans: List[LayoutSpan] = field(default_factory=list)

    # ==========================================================
    # Position
    # ==========================================================

    bbox: tuple = (0, 0, 0, 0)

    writing_direction: tuple = (1, 0)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Add Span
    # ==========================================================

    def add_span(

        self,

        span: LayoutSpan

    ):

        self.spans.append(

            span

        )

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def text(self):

        """
        Returns the complete text of the line.
        """

        return " ".join(

            span.text.strip()

            for span in self.spans

            if span.text.strip()

        )

    @property
    def span_count(self):

        return len(

            self.spans

        )

    @property
    def has_bold_text(self):

        return any(

            span.is_bold

            for span in self.spans

        )

    @property
    def has_italic_text(self):

        return any(

            span.is_italic

            for span in self.spans

        )

    @property
    def average_font_size(self):

        if not self.spans:

            return 0

        return round(

            sum(

                span.font_size

                for span in self.spans

            ) / len(self.spans),

            2

        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self):

        return {

            "text": self.text,

            "spans": self.span_count,

            "font_size": self.average_font_size,

            "bold": self.has_bold_text,

            "italic": self.has_italic_text,

            "bbox": self.bbox

        }

    # ==========================================================
    # String Representation
    # ==========================================================

    def __str__(self):

        return (

            f"LayoutLine("

            f"text='{self.text}', "

            f"spans={self.span_count}"

            f")"

        )