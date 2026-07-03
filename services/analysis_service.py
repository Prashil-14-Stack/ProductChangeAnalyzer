
import os
import shutil
from datetime import datetime
from services.semantic_repository_v2 import SemanticRepositoryV2
from utils.file_helper import FileHelper
from services.embedding_service import EmbeddingService
from comparators.parameter_comparator_v2 import ParameterComparator
from reports.excel_generator_v2 import ExcelGeneratorV2

class AnalysisService:

    def analyze(self, uploaded_files):

        if not uploaded_files:
            raise ValueError("No files uploaded.")

        if len(uploaded_files) < 2:
            raise ValueError(
                "At least two files are required."
            )

        # ===================================================
        # STEP 1
        # Read every uploaded document
        # ===================================================

        documents = []

        for index, uploaded_file in enumerate(uploaded_files):

            parameters = FileHelper.read_document(
                uploaded_file
            )

            documents.append({

                "version": index + 1,

                "filename": uploaded_file.name,

                "file_type": uploaded_file.name.split(".")[-1].lower(),

                "parameters": parameters,

                "parameter_count": len(parameters)

            })

        # ===================================================
        # STEP 2
        # Build comparison queue
        # ===================================================

        comparisons = []

        for i in range(len(documents) - 1):

            comparisons.append({

                "source": documents[i],

                "target": documents[i + 1]

            })

        # ===================================================
        # STEP 3
        # Build Semantic Repository
        # ===================================================

        repository = SemanticRepository()

        repository.build(

            documents

        )

        # ===================================================
        # STEP 4
        # Build Comparison Table
        # ===================================================

        comparator = ParameterComparator()

        comparison_table = comparator.compare(

            documents,

            repository

        )

        # ===================================================
        # STEP 4
        # Run EP5 Analysis
        # ===================================================


        analysis_results = []

        # ===================================================
        # STEP 5
        # Dashboard Metrics
        # ===================================================

        matches = sum(
            1
            for row in comparison_table
            if row["Status"] == "No Change"
        )

        changes = sum(
            1
            for row in comparison_table
            if row["Status"] != "No Change"
        )

        repository = len(documents)

        from config.ui_config import DEFAULT_AI_ACCURACY

        accuracy = DEFAULT_AI_ACCURACY    # Placeholder until EP5 calculates confidence
        # ===================================================
        # STEP 6
        # Return everything
        # ===================================================
        excel = ExcelGeneratorV2()

        from config.report_config import (
            REPORT_FOLDER,
            REPORT_NAME
        )

        report_path = f"{REPORT_FOLDER}/{REPORT_NAME}"

        excel.generate_report(

            documents=documents,

            comparison_table=comparison_table,

            analysis_results=analysis_results,

            file_name=report_path

        )
        # ==========================================
        # SAVE ANALYSIS TO REPOSITORY
        # ==========================================

        bucket_folder = "bucket"

        os.makedirs(bucket_folder, exist_ok=True)

        run_name = datetime.now().strftime(
            "Analysis_%Y%m%d_%H%M%S"
        )

        run_folder = os.path.join(
            bucket_folder,
            run_name
        )

        os.makedirs(run_folder)

        # Copy uploaded documents

        for uploaded_file in uploaded_files:

            destination = os.path.join(
                run_folder,
                uploaded_file.name
            )

            with open(destination, "wb") as f:

                f.write(uploaded_file.getbuffer())

        # Copy Excel report

        shutil.copy(

            report_path,

            os.path.join(

                run_folder,

                "Product_Analysis_Report.xlsx"

            )

        )
        return {

            "documents": documents,

            "comparison_table": comparison_table,

            "comparisons": comparisons,

            "analysis": analysis_results,

            "report_path": report_path,

            "metrics": {

                "parameters": len(comparison_table),

                "matches": matches,

                "changes": changes,

                "repository": repository,

                "accuracy": accuracy

            }

        }