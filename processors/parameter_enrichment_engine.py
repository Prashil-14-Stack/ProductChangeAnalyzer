import re

from processors.business_tokenizer import BusinessTokenizer
from processors.insurance_dictionary import InsuranceDictionary


class ParameterEnrichmentEngine:
    """
    Enterprise Parameter Enrichment Engine

    Enriches a BusinessParameter with
    NLP and insurance metadata.

    No extraction.
    No comparison.
    No AI.
    """

    def __init__(self):

        self.tokenizer = BusinessTokenizer()

        self.dictionary = InsuranceDictionary()

    # ==========================================================
    # Enrich Parameter
    # ==========================================================

    def enrich(

        self,

        parameter

    ):

        # ---------------------------------------------
        # Tokenization
        # ---------------------------------------------

        tokens = self.tokenizer.tokenize(

            parameter.value

        )

        parameter.tokens = tokens

        # ---------------------------------------------
        # Insurance Terms
        # ---------------------------------------------

        parameter.business_terms = [

            token

            for token in tokens

            if self.dictionary.is_known_term(

                token

            )

        ]

        # ---------------------------------------------
        # Numeric Values
        # ---------------------------------------------

        parameter.detected_values = re.findall(

            r"\d+(?:\.\d+)?",

            parameter.value

        )

        # ---------------------------------------------
        # Parameter Category
        # ---------------------------------------------

        parameter.category = self.detect_category(

            parameter.name

        )

        # ---------------------------------------------
        # Business Criticality
        # ---------------------------------------------

        critical_keywords = [

            "entry age",

            "maturity",

            "premium",

            "sum assured",

            "death benefit",

            "surrender",

            "policy term",

            "ppt",

            "gst",

            "tax"

        ]

        parameter.business_critical = any(

            keyword in parameter.normalized_name

            for keyword in critical_keywords

        )

        # ---------------------------------------------
        # Metadata
        # ---------------------------------------------

        parameter.metadata["token_count"] = len(

            parameter.tokens

        )

        parameter.metadata["business_term_count"] = len(

            parameter.business_terms

        )

        parameter.metadata["detected_value_count"] = len(

            parameter.detected_values

        )

        return parameter

    # ==========================================================
    # Detect Category
    # ==========================================================

    def detect_category(

        self,

        parameter_name

    ):

        name = parameter_name.lower()

        if "entry age" in name:

            return "Eligibility"

        if "maturity" in name:

            return "Maturity"

        if "premium" in name:

            return "Premium"

        if "death" in name:

            return "Benefit"

        if "surrender" in name:

            return "Surrender"

        if "rider" in name:

            return "Rider"

        if "tax" in name or "gst" in name:

            return "Tax"

        return "General"