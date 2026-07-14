from typing import List

from models.layout_block import LayoutBlock


class ReadingOrderEngine:
    """
    ==========================================================
    Enterprise Reading Order Engine

    Purpose
    -------
    Determines the logical reading order of LayoutBlocks
    on a PDF page.

    Responsibilities
    ----------------
    ✔ Sort blocks top-to-bottom
    ✔ Sort blocks left-to-right
    ✔ Detect multi-column layouts (future)
    ✔ Preserve reading sequence

    Does NOT
    --------
    ✘ Merge blocks
    ✘ Classify blocks
    ✘ Detect business parameters
    ✘ Detect tables

    ==========================================================
    """

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    Y_TOLERANCE = 8

    # ==========================================================
    # Process Document
    # ==========================================================

    def process(self, document):

        for page in document.pages:

            page.layout_blocks = self.process_page(
                page.layout_blocks
            )

        return document

    # ==========================================================
    # Process One Page
    # ==========================================================

    def process_page(

        self,

        layout_blocks: List[LayoutBlock]

    ) -> List[LayoutBlock]:

        if not layout_blocks:

            return []

        ordered = sorted(

            layout_blocks,

            key=lambda block: (

                round(block.bbox[1] / self.Y_TOLERANCE),

                block.bbox[0]

            )

        )

        # Re-number blocks
        for index, block in enumerate(

            ordered,

            start=1

        ):

            block.block_number = index

        return ordered