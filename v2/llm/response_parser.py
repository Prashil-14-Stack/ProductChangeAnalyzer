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

from v2.models.product_specification import ProductSpecification
from v2.models.business_parameter import BusinessParameter


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

            # Support both old and new prompts
            product_version=(
                data.get("version")
                or data.get("product_version", "")
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

        seen_parameters = set()

        for item in data.get("parameters", []):

            parameter = BusinessParameter(

                # Support both formats
                name=(
                    item.get("name")
                    or item.get("parameter_name", "")
                ),

                value=(
                    item.get("value")
                    or item.get("parameter_value", "")
                ),

                category=item.get(
                    "category",
                    ""
                ),

                section=item.get(
                    "section",
                    ""
                ),

                page_number=(
                    item.get("page")
                    or item.get("page_number", 0)
                ),

                confidence=item.get(
                    "confidence",
                    1.0
                )

            )

            if not self._is_valid_parameter(parameter):
                continue

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

        name = (parameter.name or "").strip()

        value = (parameter.value or "").strip()

        if not name:

            return False

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