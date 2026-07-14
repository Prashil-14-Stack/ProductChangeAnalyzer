from copy import deepcopy

from models.layout_block import LayoutBlock


class LayoutNormalizer:
    """
    ==========================================================
    Enterprise Layout Normalizer

    Converts fragmented LayoutBlocks into cleaner,
    semantically complete LayoutBlocks.

    This engine performs deterministic layout merging only.

    It does NOT perform

        ✘ AI
        ✘ OCR
        ✘ Business Detection
        ✘ Table Detection

    ==========================================================
    """

    # ----------------------------------------------------------
    # Configuration
    # ----------------------------------------------------------

    VERTICAL_GAP_THRESHOLD = 12

    FONT_SIZE_TOLERANCE = 0.5

    LEFT_ALIGNMENT_TOLERANCE = 8

    # ==========================================================
    # Normalize Document
    # ==========================================================

    def normalize(

        self,

        document

    ):

        for page in document.pages:

            page.layout_blocks = self._normalize_page(

                page.layout_blocks

            )

        return document

    # ==========================================================
    # Normalize One Page
    # ==========================================================

    def _normalize_page(

        self,

        blocks

    ):

        if not blocks:

            return []

        normalized = []

        current = deepcopy(

            blocks[0]

        )

        for nxt in blocks[1:]:

            if self._should_merge(

                current,

                nxt

            ):

                self._merge(

                    current,

                    nxt

                )

            else:

                normalized.append(

                    current

                )

                current = deepcopy(

                    nxt

                )

        normalized.append(

            current

        )

        return normalized

    # ==========================================================
    # Merge Decision
    # ==========================================================

    def _should_merge(

        self,

        block1,

        block2

    ):

        # ------------------------------------------
        # Same Font Size
        # ------------------------------------------

        if abs(

            block1.average_font_size

            -

            block2.average_font_size

        ) > self.FONT_SIZE_TOLERANCE:

            return False

        # ------------------------------------------
        # Same Left Alignment
        # ------------------------------------------

        if abs(

            block1.bbox[0]

            -

            block2.bbox[0]

        ) > self.LEFT_ALIGNMENT_TOLERANCE:

            return False

        # ------------------------------------------
        # Vertical Distance
        # ------------------------------------------

        gap = (

            block2.bbox[1]

            -

            block1.bbox[3]

        )

        if gap > self.VERTICAL_GAP_THRESHOLD:

            return False

        return True

    # ==========================================================
    # Merge Blocks
    # ==========================================================

    def _merge(

        self,

        current,

        nxt

    ):

        current.lines.extend(

            nxt.lines

        )

        current.bbox = (

            min(

                current.bbox[0],

                nxt.bbox[0]

            ),

            min(

                current.bbox[1],

                nxt.bbox[1]

            ),

            max(

                current.bbox[2],

                nxt.bbox[2]

            ),

            max(

                current.bbox[3],

                nxt.bbox[3]

            )

        )

        current.metadata.setdefault(

            "merged_blocks",

            []

        ).append(

            nxt.block_number

        )