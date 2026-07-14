from models.document import Document

from processors.business_tokenizer import BusinessTokenizer
from processors.insurance_dictionary import InsuranceDictionary
from processors.parameter_detection_engine import ParameterDetectionEngine


class ParameterExtractor:
    """
    Enterprise Parameter Extraction Engine

    Orchestrates the extraction of BusinessParameters
    from a Document.
    """

    def __init__(self):

        self.detector = ParameterDetectionEngine()

        self.tokenizer = BusinessTokenizer()

        self.dictionary = InsuranceDictionary()

    # ==========================================================
    # Extract Parameters
    # ==========================================================

    def extract(

        self,

        document: Document

    ) -> Document:

        # ----------------------------------------------
        # Clear Previous Extraction
        # ----------------------------------------------

        document.parameters.clear()

        # ----------------------------------------------
        # Every Page
        # ----------------------------------------------

        for page in document.pages:

            # ----------------------------------------------
            # Every Block
            # ----------------------------------------------

            for block in page.blocks:

                try:

                    parameter = self.detector.detect(

                        block=block,

                        page=page,

                        source_document=document.filename

                    )

                except Exception as ex:

                    print(f"Parameter Detection Error: {ex}")

                    continue

                if parameter is None:

                    continue

                # ----------------------------------------------
                # Prevent Duplicate Parameters
                # ----------------------------------------------

                existing_parameters = {

                    p.name.lower()

                    for p in document.parameters

                }

                if parameter.name.lower() in existing_parameters:

                    continue

                # ----------------------------------------------
                # NLP Tokenization
                # ----------------------------------------------

                tokens = self.tokenizer.tokenize(

                    parameter.value

                )

                parameter.tokens = tokens

                # ----------------------------------------------
                # Insurance Terms
                # ----------------------------------------------

                parameter.business_terms = [

                    token

                    for token in tokens

                    if self.dictionary.is_known_term(

                        token["value"]

                    )

                ]

                # ----------------------------------------------
                # Metadata
                # ----------------------------------------------

                parameter.metadata["token_count"] = len(

                    parameter.tokens

                )

                parameter.metadata["business_term_count"] = len(

                    parameter.business_terms

                )

                # ----------------------------------------------
                # Add Parameter to Document
                # ----------------------------------------------

                document.add_parameter(

                    parameter

                )

        return document