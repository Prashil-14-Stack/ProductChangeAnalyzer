from models.business_section import BusinessSection


class SectionDetectorPDF:
    """
    ==========================================================
    Enterprise PDF Section Detector

    Purpose
    -------
    Converts ordered LayoutBlocks into logical
    Business Sections.

    A Section begins with a HEADING and contains all
    subsequent content until the next HEADING.

    Input
    -----
    PDFDocument

    Output
    ------
    List[BusinessSection]

    ==========================================================
    """

    def detect(self, document):

        sections = []

        current_section = None

        # ------------------------------------------------------
        # Walk every page
        # ------------------------------------------------------

        for page in document.pages:

            for block in page.layout_blocks:

                block_type = getattr(

                    block,

                    "block_type",

                    "UNKNOWN"

                )

                # --------------------------------------------------
                # New Section
                # --------------------------------------------------

                if block_type == "HEADING":

                    if current_section:

                        sections.append(

                            current_section

                        )

                    current_section = BusinessSection(

                        title=block.text.strip(),

                        page_number=page.page_number

                    )

                    current_section.add_block(

                        block

                    )

                    continue

                # --------------------------------------------------
                # Ignore everything before first heading
                # --------------------------------------------------

                if current_section is None:

                    continue

                # --------------------------------------------------
                # Add block
                # --------------------------------------------------

                current_section.add_block(

                    block

                )

        # ----------------------------------------------------------
        # Last Section
        # ----------------------------------------------------------

        if current_section:

            sections.append(

                current_section

            )

        return sections