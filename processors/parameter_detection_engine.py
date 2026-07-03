import re

from models.business_parameter import BusinessParameter


class ParameterDetectionEngine:
    """
    Detects insurance business parameters from
    DocumentBlocks.

    Responsible only for identifying parameters.

    No comparison.
    No AI.
    """

    # ==========================================================
    # Detect Parameter
    # ==========================================================

    def detect(

        self,

        block,

        page,

        source_document=""

    ):

        text = block.text.strip()

        if not text:

            return None

        # ---------------------------------------------
        # Split into logical lines
        # ---------------------------------------------

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        # ---------------------------------------------
        # Not enough content
        # ---------------------------------------------

        if len(lines) < 2:

            return None

        # ---------------------------------------------
        # Parameter Name
        # ---------------------------------------------

        parameter_name = lines[0]

        # ---------------------------------------------
        # Parameter Value
        # ---------------------------------------------

        parameter_value = "\n".join(

            lines[1:]

        )

        # ---------------------------------------------
        # Build BusinessParameter
        # ---------------------------------------------

        parameter = BusinessParameter(

            name=parameter_name,

            normalized_name=self.normalize_name(

                parameter_name

            ),

            value=parameter_value,

            raw_text=text,

            page_number=page.page_number,

            block_number=block.block_number,

            source_document=source_document,

            confidence=100,

            extraction_method="Rule Based"

        )

        return parameter

    # ==========================================================
    # Normalize Parameter
    # ==========================================================

    def normalize_name(

        self,

        parameter_name

    ):

        parameter_name = parameter_name.lower()

        parameter_name = parameter_name.strip()

        parameter_name = re.sub(

            r"\s+",

            " ",

            parameter_name

        )

        return parameter_name