import re

from models.business_parameter import BusinessParameter


class BusinessParameterExtractorPDF:
    """
    ==========================================================
    Enterprise PDF Business Parameter Extractor

    Converts Business Sections into canonical
    BusinessParameter objects.

    One section can produce multiple parameters.

    ==========================================================
    """

    # ---------------------------------------------------------
    # Common Parameter Keywords
    # ---------------------------------------------------------

    PARAMETER_PATTERNS = [

        r"Entry Age",

        r"Minimum Entry Age",

        r"Maximum Entry Age",

        r"Maturity Age",

        r"Policy Term",

        r"Premium Payment Term",

        r"Premium Payment Frequency",

        r"Sum Assured",

        r"Plan Description",

        r"Death Benefit",

        r"Maturity Benefit",

        r"Surrender Benefit",

        r"Grace Period",

        r"Loan",

        r"Revival",

        r"Rider",

        r"Eligibility"

    ]

    # ==========================================================
    # Extract
    # ==========================================================

    def extract(

        self,

        sections

    ):

        parameters = []

        for section in sections:

            extracted = self._extract_from_section(

                section

            )

            parameters.extend(

                extracted

            )

        return parameters

    # ==========================================================
    # Extract One Section
    # ==========================================================

    def _extract_from_section(

        self,

        section

    ):

        parameters = []

        current_parameter = None

        current_value = []

        lines = section.text.splitlines()

        for line in lines:

            text = line.strip()

            if not text:

                continue

            # ---------------------------------------------
            # Is this a parameter?
            # ---------------------------------------------

            if self._is_parameter(

                text

            ):

                if current_parameter:

                    parameter = BusinessParameter()

                    parameter.name = current_parameter

                    parameter.value = "\n".join(

                        current_value

                    ).strip()

                    parameter.metadata = {

                        "page": section.page_number,

                        "section": section.title

                    }

                    parameters.append(

                        parameter

                    )

                current_parameter = text

                current_value = []

            else:

                current_value.append(

                    text

                )

        # ---------------------------------------------
        # Last Parameter
        # ---------------------------------------------

        if current_parameter:

            parameter = BusinessParameter()

            parameter.name = current_parameter

            parameter.value = "\n".join(

                current_value

            ).strip()

            parameter.metadata = {

                "page": section.page_number,

                "section": section.title

            }

            parameters.append(

                parameter

            )

        return parameters

    # ==========================================================
    # Parameter Detection
    # ==========================================================

    def _is_parameter(

        self,

        text

    ):

        for pattern in self.PARAMETER_PATTERNS:

            if re.search(

                pattern,

                text,

                re.IGNORECASE

            ):

                return True

        return False