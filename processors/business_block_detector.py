from models.business_block import BusinessBlock


class BusinessBlockDetectorPDF:
    """
    ==========================================================
    Enterprise PDF Business Block Detector

    Detects logical business sections from ordered
    LayoutBlocks.

    Assumptions
    -----------
    • Layout blocks are already:
        ✔ Normalized
        ✔ Reading-order sorted
        ✔ Classified

    Output
    ------
    List[BusinessBlock]

    ==========================================================
    """

    def detect(self, document):

        business_blocks = []

        current_block = None

        # ------------------------------------------------------
        # Iterate through every page
        # ------------------------------------------------------

        for page in document.pages:

            for block in page.layout_blocks:

                block_type = getattr(block, "block_type", "UNKNOWN")

                # --------------------------------------------------
                # Start of a New Business Parameter
                # --------------------------------------------------

                if block_type == "HEADING":

                    # Save previous block
                    if current_block:

                        business_blocks.append(current_block)

                    current_block = BusinessBlock()

                    current_block.parameter_name = block.text.strip()

                    current_block.page_number = page.page_number

                    current_block.confidence = (
                        block.classification_confidence
                    )

                    current_block.source_blocks.append(
                        block.block_number
                    )

                    continue

                # --------------------------------------------------
                # Ignore everything before first heading
                # --------------------------------------------------

                if current_block is None:
                    continue

                # --------------------------------------------------
                # Paragraph
                # --------------------------------------------------

                if block_type == "PARAGRAPH":

                    current_block.add_paragraph(
                        block.text
                    )

                    current_block.source_blocks.append(
                        block.block_number
                    )

                # --------------------------------------------------
                # Bullet List
                # --------------------------------------------------

                elif block_type == "BULLET":

                    current_block.add_bullet(
                        block.text
                    )

                    current_block.source_blocks.append(
                        block.block_number
                    )

                # --------------------------------------------------
                # Table
                # --------------------------------------------------

                elif block_type == "TABLE":

                    current_block.add_table(
                        block.text
                    )

                    current_block.source_blocks.append(
                        block.block_number
                    )

                # --------------------------------------------------
                # Notes
                # --------------------------------------------------

                elif block_type in [

                    "NOTE",

                    "FOOTNOTE"

                ]:

                    current_block.add_note(
                        block.text
                    )

                    current_block.source_blocks.append(
                        block.block_number
                    )

                # --------------------------------------------------
                # Unknown
                # --------------------------------------------------

                else:

                    current_block.add_paragraph(
                        block.text
                    )

                    current_block.source_blocks.append(
                        block.block_number
                    )

        # ----------------------------------------------------------
        # Last Parameter
        # ----------------------------------------------------------

        if current_block:

            business_blocks.append(

                current_block

            )

        return business_blocks