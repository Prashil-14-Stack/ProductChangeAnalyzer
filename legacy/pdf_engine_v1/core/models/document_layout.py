"""
==========================================================
Document Layout

Output of the Layout Intelligence Engine.

This model represents the logical structure of a document.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class DocumentLayout:

    pages: list = field(default_factory=list)

    sections: list = field(default_factory=list)

    tables: list = field(default_factory=list)

    figures: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    statistics: dict = field(default_factory=dict)

    @property
    def total_pages(self):

        return len(self.pages)

    @property
    def total_sections(self):

        return len(self.sections)

    @property
    def total_tables(self):

        return len(self.tables)

    @property
    def total_figures(self):

        return len(self.figures)