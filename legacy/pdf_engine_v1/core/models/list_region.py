"""
==========================================================
List Region

Represents one detected bullet or numbered list.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class ListRegion:

    page_number: int

    bbox: tuple

    list_type: str = "UNKNOWN"

    confidence: float = 0.0

    items: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_item(self, item):

        self.items.append(item)

    @property
    def text(self):

        return "\n".join(

            item.text

            for item in self.items

        )

    @property
    def item_count(self):

        return len(self.items)