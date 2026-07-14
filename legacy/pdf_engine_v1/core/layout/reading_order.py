"""
==========================================================
Enterprise Reading Order Engine

Purpose
-------
Reconstruct the natural human reading order of
layout objects.

The engine currently uses coordinate-based ordering.

Future versions will support:

✓ Multi-column layouts
✓ Tables
✓ Floating figures
✓ Side notes
✓ Complex magazine layouts

==========================================================
"""


class ReadingOrder:

    # ======================================================
    # Process
    # ======================================================

    def process(self, document):

        """
        Sort every page into natural reading order.
        """

        for page in document.pages:

            page.layout_blocks = self._sort_page(

                page.layout_blocks

            )

        return document

    # ======================================================
    # Sort One Page
    # ======================================================

    def _sort_page(

        self,

        blocks

    ):

        """
        Reading Order

        Primary Key
            Top → Bottom

        Secondary Key
            Left → Right
        """

        return sorted(

            blocks,

            key=lambda block: (

                round(block.bbox[1], 1),

                round(block.bbox[0], 1)

            )

        )