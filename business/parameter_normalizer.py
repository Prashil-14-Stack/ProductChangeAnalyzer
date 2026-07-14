"""
==========================================================
Parameter Normalizer

Purpose
-------
Normalizes extracted Business Parameters into a canonical
representation.

Examples
--------

Entry Age
Minimum Age at Entry
Min Entry Age

↓

Minimum Entry Age

This module also performs:

✓ Name normalization
✓ Value cleanup
✓ Unit extraction
✓ Confidence adjustment

==========================================================
"""

import re

from business.knowledge_loader import KnowledgeLoader


class ParameterNormalizer:

    def __init__(self):

        self.knowledge = KnowledgeLoader()

    # ======================================================
    # Process
    # ======================================================

    def process(self, document):

        if not hasattr(document, "business_parameters"):

            return document

        for parameter in document.business_parameters:

            self._normalize(parameter)

        self._debug(document)

        return document

    # ======================================================
    # Normalize One Parameter
    # ======================================================

    def _normalize(self, parameter):

        # ---------------------------------------------
        # Canonical Name
        # ---------------------------------------------

        parameter.normalized_name = (

            self.knowledge.normalize(

                parameter.name

            )

        )

        # ---------------------------------------------
        # Category
        # ---------------------------------------------

        parameter.category = (

            self.knowledge.get_category(

                parameter.normalized_name

            )

        )

        # ---------------------------------------------
        # Clean Value
        # ---------------------------------------------

        parameter.normalized_value = (

            self._normalize_value(

                parameter.value

            )

        )

        # ---------------------------------------------
        # Units
        # ---------------------------------------------

        parameter.units = self._extract_units(

            parameter.normalized_value

        )

        # ---------------------------------------------
        # Confidence
        # ---------------------------------------------

        parameter.confidence = min(

            1.0,

            parameter.confidence + 0.02

        )

    # ======================================================
    # Normalize Value
    # ======================================================

    def _normalize_value(self, value):

        if value is None:

            return ""

        value = str(value)

        value = value.strip()

        value = re.sub(

            r"\s+",

            " ",

            value

        )

        value = value.replace("Rs.", "₹")

        value = value.replace("Rs", "₹")

        value = value.replace("INR", "₹")

        return value

    # ======================================================
    # Extract Units
    # ======================================================

    def _extract_units(self, value):

        value = value.lower()

        if "%" in value:

            return "%"

        if "year" in value:

            return "Years"

        if "month" in value:

            return "Months"

        if "day" in value:

            return "Days"

        if "₹" in value:

            return "Currency"

        return ""

    # ======================================================
    # Debug
    # ======================================================

    def _debug(self, document):

        print()

        print("=" * 100)

        print("PARAMETER NORMALIZER")

        print("=" * 100)

        if not document.business_parameters:

            print("No parameters available.")

            return

        for parameter in document.business_parameters:

            print()

            print(f"Original Name     : {parameter.name}")

            print(f"Normalized Name   : {parameter.normalized_name}")

            print(f"Original Value    : {parameter.value}")

            print(f"Normalized Value  : {parameter.normalized_value}")

            print(f"Category          : {parameter.category}")

            print(f"Units             : {parameter.units}")

            print(f"Confidence        : {parameter.confidence:.2f}")