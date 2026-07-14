from models.document import Document

from processors.document_intelligence_engine import DocumentIntelligenceEngine
from processors.parameter_extractor import ParameterExtractor

from services.semantic_repository_v2 import SemanticRepositoryV2

from comparators.parameter_comparator_docx import ParameterComparatorDOCX

from reports.excel_generator_docx import ExcelGeneratorDOCX

from utils.file_helper import FileHelper


class AnalysisPipeline:

    """
    Enterprise Analysis Pipeline

    Every stage receives and returns
    a Document object.
    """

    def __init__(self):

        self.document_engine = DocumentIntelligenceEngine()

        self.parameter_extractor = ParameterExtractor()

        self.repository = SemanticRepositoryV2()

        self.comparator = ParameterComparatorDOCX()

        self.report_generator = ExcelGeneratorDOCX()

    # ==========================================================
    # Execute Pipeline
    # ==========================================================

    def execute(

        self,

        uploaded_files,

        report_path

    ):

        documents: list[Document] = []

        # ======================================================
        # Read & Process Documents
        # ======================================================

        for uploaded_file in uploaded_files:

            try:

                # ----------------------------------------------
                # Reader
                # ----------------------------------------------

                document = FileHelper.read_document(

                    uploaded_file

                )

                # ----------------------------------------------
                # Document Intelligence
                # ----------------------------------------------

                document = self.document_engine.process(

                    document

                )

                # ----------------------------------------------
                # Parameter Extraction
                # ----------------------------------------------

                document = self.parameter_extractor.extract(

                    document

                )

                # ----------------------------------------------
                # Debug Information
                # ----------------------------------------------

                print("\n" + "=" * 80)
                print(f"DOCUMENT : {document.filename}")
                print(document.summary())

                print("\nExtracted Parameters")

                for parameter in document.parameters:

                    print(f"• {parameter.name}")

                print("=" * 80 + "\n")

                documents.append(

                    document

                )

            except Exception as ex:

                print(

                    f"\n❌ Failed to process "

                    f"{uploaded_file.name}"

                )

                print(ex)

                raise

        # ======================================================
        # Validate
        # ======================================================

        if not documents:

            raise ValueError(

                "No documents were successfully processed."

            )

        # ======================================================
        # Semantic Repository
        # ======================================================

        self.repository.build(

            documents

        )

        # ======================================================
        # Comparison
        # ======================================================

        comparison_table = self.comparator.compare(

            documents,

            self.repository

        )

        # ======================================================
        # Generate Excel Report
        # ======================================================

        self.report_generator.generate_report(

            documents=documents,

            comparison_table=comparison_table,

            analysis_results=[],

            file_name=report_path

        )

        # ======================================================
        # Build Comparison Summary
        # ======================================================

        comparisons = []

        for i in range(len(documents) - 1):

            comparisons.append({

                "source": {

                    "version": documents[i].version,

                    "filename": documents[i].filename

                },

                "target": {

                    "version": documents[i + 1].version,

                    "filename": documents[i + 1].filename

                }

            })

        # ======================================================
        # Dashboard Metrics
        # ======================================================

        matches = sum(

            1

            for row in comparison_table

            if row.get("Status") == "No Change"

        )

        changes = len(comparison_table) - matches

        metrics = {

            "parameters": len(comparison_table),

            "matches": matches,

            "changes": changes,

            "repository": len(documents),

            "accuracy": 0

        }

        # ======================================================
        # Return
        # ======================================================

        return {

            "documents": documents,

            "comparison_table": comparison_table,

            "comparisons": comparisons,

            "analysis": [],

            "report_path": report_path,

            "metrics": metrics

        }