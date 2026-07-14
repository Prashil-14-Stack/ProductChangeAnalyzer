"""
==========================================================
Layout Feature Extractor

Purpose
-------
Computes layout features for every LayoutBlock.

These features are consumed by

    • LayoutClassifier
    • TableDetector
    • SectionBuilder
    • ParameterExtractor

This module DOES NOT classify.

It only computes features.

==========================================================
"""


class LayoutFeatureExtractor:

    def process(self, document):

        for page in document.pages:

            self._process_page(page)

        return document

    # ------------------------------------------------------

    def _process_page(self, page):

        page_width = page.width
        page_height = page.height

        for block in page.layout_blocks:

            block.features = {

                "line_count": self._line_count(block),

                "word_count": self._word_count(block),

                "character_count": self._character_count(block),

                "average_font_size": self._avg_font(block),

                "max_font_size": self._max_font(block),

                "is_bold": self._is_bold(block),

                "is_centered": self._is_centered(block, page_width),

                "is_left_aligned": self._is_left_aligned(block),

                "contains_numbers": self._contains_numbers(block),

                "contains_currency": self._contains_currency(block),

                "contains_percentage": self._contains_percentage(block),

                "contains_bullets": self._contains_bullets(block),

                "is_short_text": self._is_short(block),

                "left_margin": block.bbox[0],

                "top_margin": block.bbox[1],

                "width": block.bbox[2] - block.bbox[0],

                "height": block.bbox[3] - block.bbox[1],

                "width_ratio": (
                    (block.bbox[2] - block.bbox[0]) / page_width
                ),

                "height_ratio": (
                    (block.bbox[3] - block.bbox[1]) / page_height
                ),

                "reading_order": getattr(
                    block,
                    "reading_order",
                    0
                ),

                "has_previous": block.previous_block is not None,

                "has_next": block.next_block is not None,

                "inside_table": hasattr(
                    block,
                    "table_id"
                ),

                "logical_line_count": len(
                    getattr(
                        block,
                        "logical_lines",
                        []
                    )
                )
            }

    # ======================================================
    # Helpers
    # ======================================================

    def _line_count(self, block):

        return len(block.lines)

    # ------------------------------------------------------

    def _word_count(self, block):

        return len(block.text.split())

    # ------------------------------------------------------

    def _character_count(self, block):

        return len(block.text)

    # ------------------------------------------------------

    def _avg_font(self, block):

        sizes = []

        for line in block.lines:

            if hasattr(line, "raw_line"):

                sizes.append(
                    line.raw_line.average_font_size
                )

        if not sizes:

            return 0

        return sum(sizes) / len(sizes)

    # ------------------------------------------------------

    def _max_font(self, block):

        maximum = 0

        for line in block.lines:

            if hasattr(line, "raw_line"):

                maximum = max(
                    maximum,
                    line.raw_line.average_font_size
                )

        return maximum

    # ------------------------------------------------------

    def _is_bold(self, block):

        for line in block.lines:

            if hasattr(line, "raw_line"):

                if line.raw_line.is_bold:

                    return True

        return False

    # ------------------------------------------------------

    def _is_centered(self, block, page_width):

        center = (
            block.bbox[0] +
            block.bbox[2]
        ) / 2

        return abs(
            center -
            page_width / 2
        ) < 40

    # ------------------------------------------------------

    def _is_left_aligned(self, block):

        return block.bbox[0] < 120

    # ------------------------------------------------------

    def _contains_numbers(self, block):

        return any(

            c.isdigit()

            for c in block.text

        )

    # ------------------------------------------------------

    def _contains_currency(self, block):

        text = block.text.lower()

        return (

            "₹" in text or

            "rs." in text or

            "rs " in text or

            "$" in text

        )

    # ------------------------------------------------------

    def _contains_percentage(self, block):

        return "%" in block.text

    # ------------------------------------------------------

    def _contains_bullets(self, block):

        text = block.text

        bullets = [

            "•",

            "▪",

            "◦",

            "¬",

            "-"

        ]

        return any(

            b in text

            for b in bullets

        )

    # ------------------------------------------------------

    def _is_short(self, block):

        return len(block.text.split()) <= 5

    # ======================================================
    # Debug
    # ======================================================

    def debug(self, document):

        print("\n")
        print("=" * 100)
        print("LAYOUT FEATURES")
        print("=" * 100)

        for page in document.pages:

            print(f"\nPAGE {page.page_number}")

            for block in page.layout_blocks:

                print("\n")
                print("-" * 100)

                print(
                    f"Block {block.block_number}"
                )

                print(
                    block.text[:60]
                )

                for key, value in block.features.items():

                    print(
                        f"{key:25} : {value}"
                    )