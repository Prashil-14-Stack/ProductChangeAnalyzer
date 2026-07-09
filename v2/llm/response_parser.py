"""
==========================================================
Response Parser

Purpose
-------
Converts GPT JSON responses into ProductSpecification
objects.

Responsibilities
----------------
✓ Validate JSON
✓ Parse ProductSpecification
✓ Parse Business Parameters
✓ Remove invalid parameters
✓ Remove duplicate parameters

Never calls GPT.

==========================================================
"""

import json

from models.product_specification import ProductSpecification
from models.business_parameter import BusinessParameter


class ResponseParser:

    # ======================================================
    # Public
    # ======================================================

    def parse_product_specification(
        self,
        response
    ):

        data = json.loads(response)

        specification = ProductSpecification(

            product_name=data.get(
                "product_name",
                ""
            ),

            product_version=data.get(
                "product_version",
                ""
            ),

            insurer=data.get(
                "insurer",
                ""
            ),

            document_type=data.get(
                "document_type",
                ""
            )

        )

        # Track parameters already added
        seen_parameters = set()

        for item in data.get("parameters", []):

            parameter = BusinessParameter(

                name=item.get(
                    "parameter_name",
                    ""
                ),

                value=item.get(
                    "parameter_value",
                    ""
                ),

                category=item.get(
                    "category",
                    ""
                ),

                section=item.get(
                    "section",
                    ""
                ),

                page_number=item.get(
                    "page_number",
                    0
                ),

                confidence=item.get(
                    "confidence",
                    1.0
                )

            )

            # Skip invalid parameters
            if not self._is_valid_parameter(parameter):

                continue

            # Skip duplicate parameters
            key = parameter.name.strip().lower()

            if key in seen_parameters:

                continue

            seen_parameters.add(key)

            specification.add_parameter(parameter)

        return specification

    # ======================================================
    # Validation
    # ======================================================

    def validate_json(
        self,
        response
    ):

        try:

            json.loads(response)

            return True

        except Exception:

            return False

    # ======================================================
    # Helpers
    # ======================================================

    def _is_valid_parameter(
        self,
        parameter
    ):

        """
        Returns True if the parameter should be kept.
        """

        name = (parameter.name or "").strip()

        value = (parameter.value or "").strip()

        # Parameter must have a name
        if not name:

            return False

        # Ignore placeholder values
        invalid_values = {

            "",
            "-",
            "na",
            "n/a",
            "none",
            "null",
            "nil"

        }

        if value.lower() in invalid_values:

            return False

        return True