"""
==========================================================
Table Region

Represents one detected table region in a page.

==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class TableRegion:

    page_number: int

    bbox: tuple

    objects: list = field(default_factory=list)

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    def add_object(self, obj):

        self.objects.append(obj)

    @property
    def text(self):

        return "\n".join(

            obj.text

            for obj in self.objects

        )