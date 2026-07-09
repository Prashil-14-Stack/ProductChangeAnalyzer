"""
==========================================================
LLM Pipeline Integration Test

Pipeline

PDF
    ↓
PDF Reader
    ↓
Document
    ↓
Document Chunker
    ↓
LLM Service
    ↓
ProductSpecification

==========================================================
"""

from pathlib import Path

from readers.pdf_reader import PDFReader
from llm.llm_service import LLMService


def main():

    print()
    print("=" * 100)
    print("PRODUCT CHANGE ANALYZER V2")
    print("END-TO-END LLM PIPELINE TEST")
    print("=" * 100)

    # ======================================================
    # Locate Sample PDF
    # ======================================================

    sample_folder = Path("samples")

    pdf_files = list(sample_folder.glob("*.pdf"))

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF found inside samples folder."
        )

    pdf_path = pdf_files[0]

    print(f"\nReading PDF : {pdf_path.name}")

    # ======================================================
    # Read PDF
    # ======================================================

    reader = PDFReader()

    document = reader.read(pdf_path)

    print()

    print("=" * 100)
    print("DOCUMENT SUMMARY")
    print("=" * 100)

    print(f"File Name : {document.file_name}")
    print(f"Pages     : {document.page_count()}")
    print(f"Words     : {document.word_count()}")

    print()

    # ======================================================
    # LLM Extraction
    # ======================================================

    print("=" * 100)
    print("STARTING LLM EXTRACTION")
    print("=" * 100)

    llm = LLMService()

    specification = llm.extract_product_specification(
        document
    )

    # ======================================================
    # Results
    # ======================================================

    print()

    print("=" * 100)
    print("PRODUCT INFORMATION")
    print("=" * 100)

    print(f"Product Name     : {specification.product_name}")
    print(f"Version          : {specification.product_version}")
    print(f"Insurer          : {specification.insurer}")
    print(f"Product Type     : {specification.product_type}")
    print(f"Document Type    : {specification.document_type}")

    print()

    print("=" * 100)
    print("EXTRACTED PARAMETERS")
    print("=" * 100)

    print(f"Total Parameters : {specification.parameter_count()}")

    for index, parameter in enumerate(
        specification.parameters,
        start=1
    ):

        print()

        print("-" * 60)

        print(f"{index}. {parameter.name}")

        print(f"Value      : {parameter.value}")

        print(f"Category   : {parameter.category}")

        print(f"Section    : {parameter.section}")

        print(f"Page       : {parameter.page_number}")

        print(f"Confidence : {parameter.confidence}")

    print()

    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)

    summary = specification.summary()

    for key, value in summary.items():

        print(f"{key:15}: {value}")

    print()

    print("=" * 100)
    print("PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 100)


if __name__ == "__main__":

    main()