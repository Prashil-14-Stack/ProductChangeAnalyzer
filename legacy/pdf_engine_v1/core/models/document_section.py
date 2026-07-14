"""
==========================================================
Document Section

Represents one logical section within a document.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class DocumentSection:

    title: str = ""

    page_number: int = 0

    heading = None

    paragraphs: list = field(default_factory=list)

    tables: list = field(default_factory=list)

    figures: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_paragraph(self, paragraph):

        self.paragraphs.append(paragraph)

    def add_table(self, table):

        self.tables.append(table)

    def add_figure(self, figure):

        self.figures.append(figure)

    @property
    def text(self):

        return "\n".join(

            paragraph.text

            for paragraph in self.paragraphs

        )

    def summary(self):

        return {

            "title": self.title,

            "page": self.page_number,

            "paragraphs": len(self.paragraphs),

            "tables": len(self.tables),

            "figures": len(self.figures)

        }