from models.document import Document


class DocumentIntelligenceEngine:

    """
    Enterprise Document Intelligence Engine

    Responsibility
    --------------
    Performs document-level enrichment.

    Examples:
        - Classify document type
        - Detect layout
        - Extract metadata
        - Future OCR cleanup
        - Future AI document understanding

    Does NOT extract business parameters.
    """

    # ==========================================================
    # Process Document
    # ==========================================================

    def process(

        self,

        document: Document

    ) -> Document:

        # ------------------------------------------------------
        # Basic Metadata
        # ------------------------------------------------------

        document.metadata["page_count"] = document.page_count

        document.metadata["block_count"] = document.block_count

        document.metadata["table_count"] = document.table_count

        document.metadata["document_type"] = document.file_type

        # ------------------------------------------------------
        # Future Enhancements
        # ------------------------------------------------------
        #
        # - OCR cleanup
        # - Header/Footer removal
        # - Table normalization
        # - Document classification
        # - AI layout understanding
        #
        # For now we simply enrich metadata.
        #
        # ------------------------------------------------------

        return document