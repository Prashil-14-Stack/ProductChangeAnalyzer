"""
==========================================================
Heading Detector

Purpose
-------
Detect document headings using layout features.

A heading is identified using:

• Larger font size
• Bold font
• Short text
• Numbered prefixes
• Position on page

Output
------
Each LayoutBlock gets:

block.is_heading
block.heading_level

This module does NOT build sections.

==========================================================
"""

import re


class HeadingDetector:

    FONT_SIZE_MARGIN = 1.20

    MAX_HEADING_WORDS = 12

    NUMBERING_PATTERN = re.compile(
        r"^(\d+(\.\d+)*|[A-Za-z]\)|[ivxlcdmIVXLCDM]+\))"
    )

    def process(self, document):

        for page in document.pages:

            self._process_page(page)

        return document

    # --------------------------------------------------

    def _process_page(self, page):

        blocks = page.layout_blocks

        if not blocks:
            return

        average_font = self._average_font_size(blocks)

        print("\n")
        print("=" * 100)
        print("HEADING DETECTOR")
        print("=" * 100)

        for block in blocks:

            block.is_heading = False
            block.heading_level = None

            score = self._score_block(
                block,
                average_font
            )

            if score >= 3:

                block.is_heading = True

                block.heading_level = self._heading_level(
                    block,
                    average_font
                )

                print()

                print(f"Block {block.block_number}")

                print(f"Level : H{block.heading_level}")

                print(f"Score : {score}")

                print(block.text)

    # --------------------------------------------------

    def _average_font_size(self, blocks):

        total = 0
        count = 0

        for block in blocks:

            if hasattr(block, "spans"):

                for span in block.spans:

                    total += getattr(
                        span,
                        "font_size",
                        0
                    )

                    count += 1

            elif hasattr(block, "features"):

                total += block.features.get(
                    "average_font_size",
                    11
                )

                count += 1

        if count == 0:
            return 11

        return total / count

    # --------------------------------------------------

    def _score_block(

        self,

        block,

        average_font

    ):

        score = 0

        text = block.text.strip()

        words = text.split()

        features = getattr(
            block,
            "features",
            {}
        )

        font_size = features.get(
            "average_font_size",
            average_font
        )

        # Larger font

        if font_size >= average_font * self.FONT_SIZE_MARGIN:

            score += 2

        # Bold

        if features.get(

            "is_bold",

            False

        ):

            score += 2

        # Short text

        if len(words) <= self.MAX_HEADING_WORDS:

            score += 1

        # Numbered heading

        if self.NUMBERING_PATTERN.match(text):

            score += 2

        # Uppercase

        if text.isupper():

            score += 1

        return score

    # --------------------------------------------------

    def _heading_level(

        self,

        block,

        average_font

    ):

        features = getattr(

            block,

            "features",

            {}

        )

        font = features.get(

            "average_font_size",

            average_font

        )

        if font >= average_font * 1.8:

            return 1

        if font >= average_font * 1.4:

            return 2

        return 3