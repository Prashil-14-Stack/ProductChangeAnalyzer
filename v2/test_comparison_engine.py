"""
==========================================================
Comparison Engine Integration Test

Pipeline

Version1.pdf
        ↓
PDF Reader
        ↓
Document
        ↓
LLM Service
        ↓
ProductSpecification V1

Version2.pdf
        ↓
PDF Reader
        ↓
Document
        ↓
LLM Service
        ↓
ProductSpecification V2

        ↓
Comparison Engine

        ↓
Comparison Result

==========================================================
"""

from pathlib import Path

from readers.pdf_reader import PDFReader
from llm.llm_service import LLMService
from comparison.comparison_engine import ComparisonEngine


# ==========================================================
# Helpers
# ==========================================================

def extract_specification(pdf_path: Path):

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


# ==========================================================
# Main
# ==========================================================

def main():

    print()
    print("=" * 100)
    print("PRODUCT CHANGE ANALYZER V2")
    print("COMPARISON ENGINE TEST")
    print("=" * 100)

    sample_folder = Path("samples")

    version1 = sample_folder / "Version1.pdf"

    version2 = sample_folder / "Version2.pdf"

    if not version1.exists():

        raise FileNotFoundError(
            "Version1.pdf not found inside samples folder."
        )

    if not version2.exists():

        raise FileNotFoundError(
            "Version2.pdf not found inside samples folder."
        )

    # --------------------------------------------------
    # Extract Version 1
    # --------------------------------------------------

    specification_v1 = extract_specification(
        version1
    )

    # --------------------------------------------------
    # Extract Version 2
    # --------------------------------------------------

    specification_v2 = extract_specification(
        version2
    )

    # --------------------------------------------------
    # Compare
    # --------------------------------------------------

    print()
    print("=" * 100)
    print("STARTING COMPARISON")
    print("=" * 100)

    engine = ComparisonEngine()

    result = engine.compare(
        specification_v1,
        specification_v2
    )

    # --------------------------------------------------
    # Print Summary
    # --------------------------------------------------

    print()

    result.print_summary()

    # --------------------------------------------------
    # Print Detailed Results
    # --------------------------------------------------

    print()
    print("=" * 100)
    print("COMPARISON DETAILS")
    print("=" * 100)

    for item in result.items:

        print()

        print("-" * 80)

        print(f"Parameter : {item.parameter_name}")

        print(f"Status    : {item.status}")

        print(f"Impact    : {item.impact}")

        print(f"Category  : {item.category}")

        print(f"Section   : {item.section}")

        print(f"Old Value : {item.old_value}")

        print(f"New Value : {item.new_value}")

        print(f"Reason    : {item.reason}")

    print()

    print("=" * 100)
    print("COMPARISON COMPLETED SUCCESSFULLY")
    print("=" * 100)


if __name__ == "__main__":

    main()