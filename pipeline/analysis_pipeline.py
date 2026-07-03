from processors.document_intelligence_engine import DocumentIntelligenceEngine
from processors.parameter_extractor import ParameterExtractor

from services.semantic_repository_v2 import SemanticRepositoryV2

from comparators.parameter_comparator_v2 import ParameterComparator

from reports.excel_generator_v2 import ExcelGeneratorV2

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

        self.repository = SemanticRepository()

        self.comparator = ParameterComparator()

        self.report_generator = ExcelGeneratorV2()

    # ==========================================================
    # Execute Pipeline
    # ==========================================================

    def execute(

        self,

        uploaded_files,

        report_path

    ):

        documents = []

        # ======================================================
        # Read & Process Documents
        # ======================================================

        for uploaded_file in uploaded_files:

            # ----------------------------------------------
            # Reader returns Document
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

            documents.append(

                document

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
        # Report
        # ======================================================

        self.report_generator.generate_report(

            documents=documents,

            comparison_table=comparison_table,

            analysis_results=[],

            file_name=report_path

        )

        # ======================================================
        # Return
        # ======================================================

        return {

            "documents": documents,

            "comparison_table": comparison_table,

            "report_path": report_path

        }