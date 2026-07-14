"""
==========================================================
Layout Visualizer

Draws every detected layout object on top of the
original PDF.

Purpose
-------
Debug the Layout Engine visually.

==========================================================
"""

import fitz

import os


class LayoutVisualizer:

    COLORS = {

        "HEADING": (0, 1, 0),          # Green

        "PARAGRAPH": (0, 0, 1),        # Blue

        "TABLE": (1, 0, 0),            # Red

        "LIST": (1, 0, 1),             # Purple

        "FIGURE": (1, 0.5, 0),         # Orange

        "HEADER": (0, 1, 1),

        "FOOTER": (0.4, 0.4, 0.4),

        "UNKNOWN": (1, 1, 0),

        "EMPTY": (0.8, 0.8, 0.8)

    }

    # ==================================================

    def visualize(

        self,

        pdf_path,

        document,

        output_folder="debug_output"

    ):

        os.makedirs(output_folder, exist_ok=True)
        pdf = fitz.open(pdf_path)

        for page in document.pages:

            pdf_page = pdf.load_page(

                page.page_number - 1

            )

            for block in page.layout_blocks:

                self._draw_block(

                    pdf_page,

                    block

                )

        output_pdf = f"{output_folder}/layout_debug.pdf"

        pdf.save(output_pdf)

        pdf.close()

        print()

        print("=" * 80)

        print("Layout visualization saved")

        print(output_pdf)

        print("=" * 80)

    # ==================================================

    def _draw_block(

        self,

        page,

        block

    ):

        color = self.COLORS.get(

            block.block_type,

            (1, 1, 0)

        )

        rect = fitz.Rect(

            *block.bbox

        )

        page.draw_rect(

            rect,

            color=color,

            width=1

        )

        label = f"{block.block_number} {block.block_type}"

        page.insert_text(

            (

                rect.x0,

                max(

                    rect.y0 - 4,

                    5

                )

            ),

            label,

            fontsize=7,

            color=color

        )