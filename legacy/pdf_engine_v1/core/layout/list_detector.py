"""
==========================================================
Enterprise List Detector

Purpose
-------
Detect bullet and numbered lists from layout objects.

This detector DOES NOT understand the business meaning
of the list. It only identifies list regions.

==========================================================
"""

import re

from legacy.pdf_engine_v1.core.models.list_region import ListRegion


class ListDetector:

    BULLET_PATTERNS = [

        r"^\u2022",      # •
        r"^\-",          # -
        r"^\*",          # *
        r"^▪",
        r"^○",
        r"^✓",

        r"^\d+\.",       # 1.
        r"^\d+\)",       # 1)

        r"^[a-zA-Z]\)",  # a)

        r"^[ivxlcdm]+\.",

        r"^[IVXLCDM]+\."
    ]

    # ==================================================
    # Process
    # ==================================================

    def process(self, document):

        document.lists = []

        for page in document.pages:

            lists = self._detect_lists(page)

            document.lists.extend(lists)

        return document

    # ==================================================
    # Detect Lists
    # ==================================================

    def _detect_lists(self, page):

        detected_lists = []

        current_list = None

        for block in page.layout_blocks:

            if self._is_list_item(block):

                if current_list is None:

                    current_list = ListRegion(

                        page_number=page.page_number,

                        bbox=block.bbox,

                        confidence=0.80

                    )

                current_list.add_item(block)

            else:

                if current_list:

                    detected_lists.append(current_list)

                    current_list = None

        if current_list:

            detected_lists.append(current_list)

        return detected_lists

    # ==================================================
    # List Item Detection
    # ==================================================

    def _is_list_item(self, block):

        text = block.text.strip()

        if not text:

            return False

        for pattern in self.BULLET_PATTERNS:

            if re.match(pattern, text):

                return True

        return False