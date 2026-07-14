from models.business_parameter import BusinessParameter


class BusinessParameterBuilderPDF:
    """
    ==========================================================
    Enterprise PDF Business Parameter Builder

    Converts BusinessBlocks into canonical
    BusinessParameter objects.

    Input
    -----
    List[BusinessBlock]

    Output
    ------
    List[BusinessParameter]

    ==========================================================
    """

    # ==========================================================
    # Build
    # ==========================================================

    def build(

        self,

        business_blocks

    ):

        parameters = []

        for block in business_blocks:

            parameter = BusinessParameter()

            # --------------------------------------------------
            # Identity
            # --------------------------------------------------

            parameter.name = block.parameter_name

            # --------------------------------------------------
            # Description
            # --------------------------------------------------

            description = []

            # Paragraphs
            if block.paragraphs:

                description.extend(

                    block.paragraphs

                )

            # Bullet Lists
            if block.bullet_lists:

                description.append("")

                description.append("Bullet Points:")

                description.extend(

                    block.bullet_lists

                )

            # Tables
            if block.tables:

                description.append("")

                description.append("Tables:")

                for table in block.tables:

                    description.append(

                        str(table)

                    )

            # Notes
            if block.notes:

                description.append("")

                description.append("Notes:")

                description.extend(

                    block.notes

                )

            parameter.value = "\n".join(

                description

            ).strip()

            # --------------------------------------------------
            # Metadata
            # --------------------------------------------------

            parameter.metadata = {

                "page": block.page_number,

                "confidence": block.confidence,

                "source_blocks": block.source_blocks,

                "paragraph_count": len(block.paragraphs),

                "bullet_count": len(block.bullet_lists),

                "table_count": len(block.tables),

                "note_count": len(block.notes)

            }

            parameters.append(

                parameter

            )

        return parameters