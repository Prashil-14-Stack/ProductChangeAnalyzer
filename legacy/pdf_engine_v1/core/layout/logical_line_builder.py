"""
==========================================================
Logical Line Builder

Purpose
-------
Converts physical RawLines into Logical Lines.

PyMuPDF extracts PHYSICAL lines.

Example

Income Benefit
after deferment
period

↓

Income Benefit after deferment period

The builder does NOT classify.

It only merges lines that clearly belong together.

==========================================================
"""

from copy import deepcopy


class LogicalLineBuilder:

    def __init__(self):

        self.max_vertical_gap = 4.0

        self.max_left_difference = 10.0

    # ------------------------------------------------------
    # Process Entire Document
    # ------------------------------------------------------

    def process(self, document):

        for page in document.pages:

            self._process_page(page)

        return document

    # ------------------------------------------------------
    # Process One Page
    # ------------------------------------------------------

    def _process_page(self, page):

        for block in page.layout_blocks:

            if not hasattr(block, "lines"):

                continue

            logical_lines = self._merge_lines(block.lines)

            block.logical_lines = logical_lines

    # ------------------------------------------------------
    # Merge Raw Lines
    # ------------------------------------------------------

    def _merge_lines(self, lines):

        if not lines:

            return []

        logical = []

        current = deepcopy(lines[0])

        for next_line in lines[1:]:

            if self._should_merge(current, next_line):

                self._merge(current, next_line)

            else:

                logical.append(current)

                current = deepcopy(next_line)

        logical.append(current)

        return logical

    # ------------------------------------------------------
    # Merge Decision
    # ------------------------------------------------------

    def _should_merge(self, line1, line2):

        # ----------------------------------------------
        # Font mismatch
        # ----------------------------------------------

        if line1.raw_line.dominant_font != line2.raw_line.dominant_font:

            return False

        # ----------------------------------------------
        # Size mismatch
        # ----------------------------------------------

        if abs(

            line1.raw_line.average_font_size

            -

            line2.raw_line.average_font_size

        ) > 0.5:

            return False

        # ----------------------------------------------
        # Left alignment
        # ----------------------------------------------

        if abs(

            line1.bbox[0]

            -

            line2.bbox[0]

        ) > self.max_left_difference:

            return False

        # ----------------------------------------------
        # Vertical Gap
        # ----------------------------------------------

        gap = (

            line2.bbox[1]

            -

            line1.bbox[3]

        )

        if gap > self.max_vertical_gap:

            return False

        return True

    # ------------------------------------------------------
    # Merge Two Lines
    # ------------------------------------------------------

    def _merge(self, current, nxt):

        current.text = (

            current.text.rstrip()

            + " "

            + nxt.text.lstrip()

        )

        current.raw_line.spans.extend(

            nxt.raw_line.spans

        )

        current.raw_line._update_bbox()

        x0 = min(

            current.bbox[0],

            nxt.bbox[0]

        )

        y0 = min(

            current.bbox[1],

            nxt.bbox[1]

        )

        x1 = max(

            current.bbox[2],

            nxt.bbox[2]

        )

        y1 = max(

            current.bbox[3],

            nxt.bbox[3]

        )

        current.bbox = (

            x0,

            y0,

            x1,

            y1

        )

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------

    def debug(self, document):

        print("\n")
        print("=" * 100)
        print("LOGICAL LINE BUILDER")
        print("=" * 100)

        for page in document.pages:

            print(f"\nPAGE {page.page_number}")

            for block in page.layout_blocks:

                logical = getattr(

                    block,

                    "logical_lines",

                    []

                )

                if not logical:

                    continue

                print()

                print(f"BLOCK {block.block_number}")

                for index, line in enumerate(logical, 1):

                    print(

                        f"{index:02d}.",

                        line.text

                    )

        self.logical_line_builder.debug(document)