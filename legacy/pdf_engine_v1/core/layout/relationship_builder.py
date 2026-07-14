"""
==========================================================
Relationship Builder

Purpose
-------
Build spatial relationships between layout blocks.

This processor does NOT classify blocks.

It simply enriches every block with information such as:

• Previous Block
• Next Block
• Left Neighbour
• Right Neighbour
• Top Neighbour
• Bottom Neighbour

These relationships are later consumed by

    • LayoutClassifier
    • TableDetector
    • SectionBuilder

==========================================================
"""

from math import inf


class RelationshipBuilder:

    # ------------------------------------------------------
    # Process Entire Document
    # ------------------------------------------------------

    def process(self, document):

        for page in document.pages:

            self._build_relationships(page)

        return document

    # ------------------------------------------------------
    # Build Relationships For One Page
    # ------------------------------------------------------

    def _build_relationships(self, page):

        blocks = page.layout_blocks

        if not blocks:
            return

        # ------------------------------------------
        # Reading Order
        # ------------------------------------------

        blocks.sort(
            key=lambda b: (
                round(b.bbox[1], 1),
                round(b.bbox[0], 1)
            )
        )

        for index, block in enumerate(blocks):

            block.reading_order = index + 1

            block.previous_block = (
                blocks[index - 1]
                if index > 0
                else None
            )

            block.next_block = (
                blocks[index + 1]
                if index < len(blocks) - 1
                else None
            )

        # ------------------------------------------
        # Spatial Relationships
        # ------------------------------------------

        for block in blocks:

            block.left_neighbor = self._find_left(block, blocks)

            block.right_neighbor = self._find_right(block, blocks)

            block.top_neighbor = self._find_top(block, blocks)

            block.bottom_neighbor = self._find_bottom(block, blocks)

        # ------------------------------------------
        # Debug Output
        # ------------------------------------------

        print("\n")
        print("=" * 100)
        print(f"RELATIONSHIP BUILDER - PAGE {page.page_number}")
        print("=" * 100)

        for block in blocks:

            print("\n" + "-" * 80)

            print(f"Block Number   : {block.block_number}")

            print(f"Block Type     : {getattr(block, 'block_type', 'UNKNOWN')}")

            print(f"Reading Order  : {block.reading_order}")

            print(f"Text           : {block.text[:80]}")

            print(f"BBOX           : {block.bbox}")

            print()

            print(
                "Previous Block :",
                block.previous_block.block_number
                if block.previous_block else None
            )

            print(
                "Next Block     :",
                block.next_block.block_number
                if block.next_block else None
            )

            print(
                "Left Neighbor  :",
                block.left_neighbor.block_number
                if block.left_neighbor else None
            )

            print(
                "Right Neighbor :",
                block.right_neighbor.block_number
                if block.right_neighbor else None
            )

            print(
                "Top Neighbor   :",
                block.top_neighbor.block_number
                if block.top_neighbor else None
            )

            print(
                "Bottom Neighbor:",
                block.bottom_neighbor.block_number
                if block.bottom_neighbor else None
            )

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def _find_left(self, current, blocks):

        nearest = None
        distance = inf

        for block in blocks:

            if block is current:
                continue

            if block.bbox[2] <= current.bbox[0]:

                d = current.bbox[0] - block.bbox[2]

                if d < distance:

                    distance = d
                    nearest = block

        return nearest

    # ------------------------------------------------------

    def _find_right(self, current, blocks):

        nearest = None
        distance = inf

        for block in blocks:

            if block is current:
                continue

            if block.bbox[0] >= current.bbox[2]:

                d = block.bbox[0] - current.bbox[2]

                if d < distance:

                    distance = d
                    nearest = block

        return nearest

    # ------------------------------------------------------

    def _find_top(self, current, blocks):

        nearest = None
        distance = inf

        for block in blocks:

            if block is current:
                continue

            if block.bbox[3] <= current.bbox[1]:

                d = current.bbox[1] - block.bbox[3]

                if d < distance:

                    distance = d
                    nearest = block

        return nearest

    # ------------------------------------------------------

    def _find_bottom(self, current, blocks):

        nearest = None
        distance = inf

        for block in blocks:

            if block is current:
                continue

            if block.bbox[1] >= current.bbox[3]:

                d = block.bbox[1] - current.bbox[3]

                if d < distance:

                    distance = d
                    nearest = block

        return nearest