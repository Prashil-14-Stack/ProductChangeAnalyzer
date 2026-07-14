from readers.word_reader import WordReader

from services.semantic_repository import SemanticRepository

from comparators.parameter_comparator_docx import ParameterComparatorDOCX

from reports.excel_generator_docx import ExcelGeneratorDOCX


class AnalysisPipelineDOCX:
    """
    Stable DOCX Analysis Pipeline

    DOCX

        ↓

    WordReader

        ↓

    SemanticRepository

        ↓

    ParameterComparatorDOCX

        ↓

    ExcelGeneratorDOCX
    """

    def __init__(self):

        self.reader = WordReader()

        self.repository = SemanticRepository()

        self.comparator = ParameterComparatorDOCX()

        self.report_generator = ExcelGeneratorDOCX()

    # ======================================================
    # Execute
    # ======================================================

    def execute(

        self,

        uploaded_files,

        report_path

    ):

        if len(uploaded_files) < 2:

            raise ValueError(

                "Please upload at least two DOCX files."

            )

        documents = []

        # ==================================================
        # Read Documents
        # ==================================================

        for index, uploaded_file in enumerate(

            uploaded_files,

            start=1

        ):

            parameters = self.reader.read(

                uploaded_file

            )

            documents.append({

                "version": index,

                "filename": uploaded_file.name,

                "parameters": parameters

            })

        # ==================================================
        # Build Semantic Repository
        # ==================================================

        self.repository.build(

            documents

        )

        # ==================================================
        # Compare Documents
        # ==================================================

        comparison_table = self.comparator.compare(

            documents,

            self.repository

        )

        # ==================================================
        # Generate Excel Report
        # ==================================================

        self.report_generator.generate_report(

            documents=documents,

            comparison_table=comparison_table,

            analysis_results=[],

            file_name=report_path

        )

        # ==================================================
        # Planned Comparisons
        # ==================================================

        comparisons = []

        for i in range(

            len(documents) - 1

        ):

            comparisons.append({

                "source": {

                    "version": documents[i]["version"],

                    "filename": documents[i]["filename"]

                },

                "target": {

                    "version": documents[i + 1]["version"],

                    "filename": documents[i + 1]["filename"]

                }

            })

        # ==================================================
        # Dashboard Metrics
        # ==================================================

        matches = sum(

            1

            for row in comparison_table

            if row.get("Status") == "No Change"

        )

        changes = len(

            comparison_table

        ) - matches

        metrics = {

            "parameters": len(

                comparison_table

            ),

            "matches": matches,

            "changes": changes,

            "repository": len(documents),

            "accuracy": 0

        }

        # ==================================================
        # Return
        # ==================================================

        return {

            "documents": documents,

            "comparison_table": comparison_table,

            "comparisons": comparisons,

            "analysis": [],

            "report_path": report_path,

            "metrics": metrics

        }