"""
==========================================================
Parameter Normalizer

Purpose
-------
Standardizes extracted BusinessParameters before
comparison.

Responsibilities
----------------
✓ Clean parameter names
✓ Normalize aliases
✓ Remove OCR artefacts
✓ Normalize spacing
✓ Normalize abbreviations
✓ Produce canonical parameter names

This class NEVER compares parameters.

==========================================================
"""

import re

from v2.knowledge.knowledge_loader import KnowledgeLoader


class ParameterNormalizer:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.knowledge_loader = KnowledgeLoader()

    # ======================================================
    # Public
    # ======================================================

    def normalize_specification(
        self,
        specification
    ):

        """
        Normalizes every BusinessParameter
        inside a ProductSpecification.
        """

        for parameter in specification.parameters:

            parameter.name = self.normalize_name(
                parameter.name
            )

            parameter.value = self.normalize_value(
                parameter.value
            )

            parameter.section = self.normalize_section(
                parameter.section
            )

        return specification

    # ======================================================
    # Name Normalization
    # ======================================================

    def normalize_name(
        self,
        name
    ):

        if not name:
            return ""

        name = self._clean_text(name)

        # Canonical alias lookup
        name = self.knowledge_loader.get_canonical_name(
            name
        )

        # Expand abbreviations
        name = self._expand_abbreviations(name)

        # Pattern normalization
        name = self._normalize_patterns(name)

        return name.strip()

    # ======================================================
    # Value Normalization
    # ======================================================

    def normalize_value(
        self,
        value
    ):

        if not value:
            return ""

        value = self._clean_text(value)

        return value

    # ======================================================
    # Section Normalization
    # ======================================================

    def normalize_section(
        self,
        section
    ):

        if not section:
            return ""

        return self._clean_text(section)

    # ======================================================
    # Helpers
    # ======================================================

    def _clean_text(
        self,
        text
    ):

        text = str(text)

        # Remove OCR garbage
        text = text.replace("##", "")

        text = text.replace("�", "")

        # Collapse whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ------------------------------------------------------

    def _expand_abbreviations(
        self,
        text
    ):

        replacements = {

            "PT": "Policy Term",

            "PPT": "Premium Payment Term",

            "SA": "Sum Assured",

            "ROP": "Return of Premium",

            "DB": "Death Benefit",

            "POS": "Point of Sale"

        }

        for key, value in replacements.items():

            text = re.sub(

                rf"\b{key}\b",

                value,

                text,

                flags=re.IGNORECASE

            )

        return text

    # ------------------------------------------------------

    def _normalize_patterns(
        self,
        text
    ):

        patterns = {

            r"Death Benefit during Policy Term":
                "Death Benefit",

            r"Death Benefit during PT":
                "Death Benefit",

            r"Surrender during PT":
                "Surrender Benefit",

            r"Lumpsum Benefit at Maturity":
                "Maturity Benefit",

            r"Income Benefit after deferment period":
                "Income Benefit",

            r"Maximum Policy Term for Point of Sale channel":
                "Maximum Policy Term (POS)",

            r"Maximum Policy Term for POS channel":
                "Maximum Policy Term (POS)",

            r"Maximum Sum Assured for Point of Sale channel":
                "Maximum Sum Assured (POS)",

            r"Maximum Sum Assured for POS channel":
                "Maximum Sum Assured (POS)",

            r"Maximum Maturity Age for POS channel":
                "Maximum Maturity Age (POS)",

            r"Income Instalment Frequency Change":
                "Income Instalment Frequency",

            r"Change of Income Instalment Frequency":
                "Income Instalment Frequency",

            r"Option to change Income Instalment date":
                "Income Instalment Date Change"

        }

        for pattern, replacement in patterns.items():

            if re.fullmatch(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                return replacement

        return text