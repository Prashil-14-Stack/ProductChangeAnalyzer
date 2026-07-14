"""
==========================================================
Document Section

Represents one logical section of a document.

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

    lists: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    # ------------------------------------------------------

    def add_paragraph(self, obj):

        self.paragraphs.append(obj)

    def add_table(self, table):

        self.tables.append(table)

    def add_figure(self, figure):

        self.figures.append(figure)

    def add_list(self, list_region):

        self.lists.append(list_region)

    # ------------------------------------------------------

    @property
    def text(self):

        text = []

        for p in self.paragraphs:

            text.append(p.text)

        return "\n".join(text)

    # ------------------------------------------------------

    def summary(self):

        return {

            "title": self.title,

            "page": self.page_number,

            "paragraphs": len(self.paragraphs),

            "tables": len(self.tables),

            "figures": len(self.figures),

            "lists": len(self.lists)

        }