from dataclasses import dataclass, field


@dataclass
class BusinessSection:
    """
    ==========================================================
    Business Section

    Represents one logical section in a Product
    Specification.

    Example

    Plan Description

        Paragraph

        Paragraph

        Table

        Bullet

    ==========================================================
    """

    title: str = ""

    page_number: int = 0

    blocks: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_block(

        self,

        block

    ):

        self.blocks.append(

            block

        )

    @property
    def text(self):

        return "\n".join(

            block.text

            for block in self.blocks

        )

    def summary(self):

        return {

            "title": self.title,

            "page": self.page_number,

            "blocks": len(self.blocks)

        }