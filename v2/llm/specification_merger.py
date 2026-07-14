"""
==========================================================
Specification Merger

Purpose
-------
Merge multiple partial ProductSpecification objects
into one consolidated ProductSpecification.

Each partial specification typically represents the
extraction result from one document chunk.

Responsibilities
----------------
✓ Merge product metadata
✓ Merge parameters
✓ Preserve extraction metadata

This class DOES NOT

✗ Call GPT
✗ Compare products
✗ Normalize parameters

==========================================================
"""

from v2.models.product_specification import ProductSpecification


class SpecificationMerger:

    """
    Merge multiple ProductSpecification objects.
    """

    # ======================================================
    # Public
    # ======================================================

    def merge(self, specifications):

        if not specifications:

            raise ValueError(
                "No ProductSpecifications supplied."
            )

        if len(specifications) == 1:

            return specifications[0]

        merged = ProductSpecification()

        # --------------------------------------------------
        # Product Information
        # --------------------------------------------------

        merged.product_name = self._first_non_empty(
            specifications,
            "product_name"
        )

        merged.product_version = self._first_non_empty(
            specifications,
            "product_version"
        )

        merged.insurer = self._first_non_empty(
            specifications,
            "insurer"
        )

        merged.product_type = self._first_non_empty(
            specifications,
            "product_type"
        )

        merged.document_type = self._first_non_empty(
            specifications,
            "document_type"
        )

        merged.source_file = self._first_non_empty(
            specifications,
            "source_file"
        )

        merged.source_format = self._first_non_empty(
            specifications,
            "source_format"
        )

        merged.total_pages = max(
            spec.total_pages
            for spec in specifications
        )

        merged.extraction_model = self._first_non_empty(
            specifications,
            "extraction_model"
        )

        # --------------------------------------------------
        # Merge Parameters
        # --------------------------------------------------

        seen = set()

        for specification in specifications:

            for parameter in specification.parameters:

                key = (
                    parameter.name.strip().lower(),
                    parameter.value.strip().lower()
                )

                if key in seen:
                    continue

                seen.add(key)

                merged.add_parameter(parameter)

        # --------------------------------------------------
        # Merge Metadata
        # --------------------------------------------------

        merged.metadata["merged_chunks"] = len(specifications)

        merged.metadata["merged_parameters"] = (
            merged.parameter_count()
        )

        return merged

    # ======================================================
    # Private
    # ======================================================

    def _first_non_empty(
        self,
        specifications,
        attribute
    ):

        for specification in specifications:

            value = getattr(
                specification,
                attribute,
                ""
            )

            if value:

                return value

        return ""