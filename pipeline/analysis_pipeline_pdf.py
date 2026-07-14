from processors.pdf_mvp_extractor import PDFMVPExtractor


class AnalysisPipelinePDF:
    """
    ==========================================================
    Enterprise PDF Analysis Pipeline

    Sprint 3 - Phase 1

    Responsibilities
    ----------------
    ✔ Read PDF
    ✔ Extract Business Parameters
    ✔ Return Results

    Future Phases
    -------------
    • Semantic Repository
    • Comparator
    • AI Analysis
    • Excel Report

    ==========================================================
    """

    def __init__(self):

        self.extractor = PDFMVPExtractor()

    # ==========================================================
    # Execute Pipeline
    # ==========================================================

    def execute(

        self,

        uploaded_files,

        report_path=None

    ):

        documents = []

        for version, uploaded_file in enumerate(

            uploaded_files,

            start=1

        ):

            parameters = self.extractor.extract(

                uploaded_file

            )

            documents.append(

                {

                    "version": version,

                    "filename": uploaded_file.name,

                    "parameters": parameters

                }

            )

        # ------------------------------------------------------
        # Metrics
        # ------------------------------------------------------

        total_parameters = sum(

            len(document["parameters"])

            for document in documents

        )

        metrics = {

            "documents": len(documents),

            "parameters": total_parameters

        }

        # ------------------------------------------------------
        # Return
        # ------------------------------------------------------

        return {

            "documents": documents,

            "metrics": metrics

        }