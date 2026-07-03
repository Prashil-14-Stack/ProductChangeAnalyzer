from typing import Dict, Any


class DocumentIntelligenceEngine:

    """
    Converts raw document content into a unified structure
    regardless of the source document type.

    Supported Sources

    - DOCX
    - PDF
    - OCR (future)
    """

    def process(

        self,

        raw_content: Dict[str, str],

        source_type: str

    ) -> Dict[str, Any]:

        """
        Normalizes raw document content into a common format.

        Parameters
        ----------
        raw_content
            Raw output returned by the reader.

        source_type
            docx / pdf / image

        Returns
        -------
        Unified document structure.
        """

        unified_document = {

            "source_type": source_type,

            "sections": [],

            "raw_parameters": raw_content,

            "metadata": {

                "parameter_count": len(raw_content)

            }

        }

        # ---------------------------------------
        # Convert every parameter into a section
        # ---------------------------------------

        for parameter, value in raw_content.items():

            unified_document["sections"].append({

                "parameter": parameter,

                "content": value,

                "normalized_parameter": parameter.lower().strip()

            })

        return unified_document