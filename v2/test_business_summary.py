"""
==========================================================
Business Summary Integration Test

Pipeline

Version1.pdf
        ↓
LLM Extraction
        ↓
ProductSpecification V1

Version2.pdf
        ↓
LLM Extraction
        ↓
ProductSpecification V2

        ↓
Comparison Engine

        ↓
ComparisonResult

        ↓
Business Summary Generator

==========================================================
"""

from pathlib import Path

from readers.pdf_reader import PDFReader
from llm.llm_service import LLMService
from comparison.comparison_engine import ComparisonEngine
from ai.business_summary_generator import BusinessSummaryGenerator


# ======================================================
# Helpers
# ======================================================

def extract_specification(pdf_path):

    print()
    print("=" * 80)
    print(f"Processing : {pdf_path.name}")
    print("=" * 80)

    reader = PDFReader()

    document = reader.read(pdf_path)

    llm = LLMService()

    specification = llm.extract_product_specification(
        document
    )

    print(
        f"Extracted Parameters : "
        f"{specification.parameter_count()}"
    )

    return specification


# ======================================================
# Main
# ======================================================

def main():

    print()
    print("=" * 100)
    print("PRODUCT CHANGE ANALYZER V2")
    print("BUSINESS SUMMARY TEST")
    print("=" * 100)

    sample_folder = Path("samples")

    version1 = sample_folder / "Version1.pdf"
    version2 = sample_folder / "Version2.pdf"

    if not version1.exists():

        raise FileNotFoundError(
            "Version1.pdf not found."
        )

    if not version2.exists():

        raise FileNotFoundError(
            "Version2.pdf not found."
        )

    # --------------------------------------------------
    # Extract Specifications
    # --------------------------------------------------

    specification_v1 = extract_specification(version1)

    specification_v2 = extract_specification(version2)

    # --------------------------------------------------
    # Compare Products
    # --------------------------------------------------

    print()
    print("=" * 100)
    print("COMPARING PRODUCTS")
    print("=" * 100)

    comparison_engine = ComparisonEngine()

    comparison_result = comparison_engine.compare(

        specification_v1,

        specification_v2

    )

    # --------------------------------------------------
    # Generate AI Business Summary
    # --------------------------------------------------

    print()
    print("=" * 100)
    print("GENERATING AI BUSINESS SUMMARY")
    print("=" * 100)

    generator = BusinessSummaryGenerator()

    summary = generator.generate(
        comparison_result
    )

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    print()

    print("=" * 100)
    print("AI EXECUTIVE SUMMARY")
    print("=" * 100)

    print(summary)

    print()

    print("=" * 100)
    print("BUSINESS SUMMARY GENERATED SUCCESSFULLY")
    print("=" * 100)


if __name__ == "__main__":

    main()