from dataclasses import dataclass, field
from typing import List, Dict

from models.layout_block import LayoutBlock


@dataclass
class PDFPage:
    """
    ==========================================================
    Enterprise PDF Page

    Represents one page of a PDF document.

    A page contains:

        • Layout Blocks
        • Images
        • Tables
        • Page Metadata

    The page itself performs no business logic.
    It is simply the canonical representation of
    a PDF page.

    ==========================================================
    """

    # ==========================================================
    # Page Information
    # ==========================================================

    page_number: int

    width: float

    height: float

    # ==========================================================
    # Layout
    # ==========================================================

    layout_blocks: List[LayoutBlock] = field(default_factory=list)

    # ==========================================================
    # Other Objects
    # ==========================================================

    images: List[Dict] = field(default_factory=list)

    tables: List[Dict] = field(default_factory=list)

    # ==========================================================
    # Classification
    # ==========================================================

    page_type: str = "UNKNOWN"

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Add Layout Block
    # ==========================================================

    def add_layout_block(

        self,

        block: LayoutBlock

    ):

        self.layout_blocks.append(

            block

        )

    # ==========================================================
    # Add Image
    # ==========================================================

    def add_image(

        self,

        image

    ):

        self.images.append(

            image

        )

    # ==========================================================
    # Add Table
    # ==========================================================

    def add_table(

        self,

        table

    ):

        self.tables.append(

            table

        )

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def block_count(self):

        return len(

            self.layout_blocks

        )

    @property
    def image_count(self):

        return len(

            self.images

        )

    @property
    def table_count(self):

        return len(

            self.tables

        )

    @property
    def text(self):

        """
        Complete text on the page.
        """

        return "\n\n".join(

            block.text

            for block in self.layout_blocks

            if block.text.strip()

        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self):

        return {

            "page": self.page_number,

            "layout": self.page_type,

            "blocks": self.block_count,

            "tables": self.table_count,

            "images": self.image_count,

            "width": self.width,

            "height": self.height

        }

    # ==========================================================
    # String Representation
    # ==========================================================

    def __str__(self):

        return (

            f"PDFPage("

            f"page={self.page_number}, "

            f"blocks={self.block_count}, "

            f"tables={self.table_count}, "

            f"images={self.image_count}"

            f")"

        )