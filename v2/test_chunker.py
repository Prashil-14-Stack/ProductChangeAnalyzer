"""
==========================================================
Document Chunker Test

Purpose
-------
Verify that:

✓ PDFReader reads the PDF correctly
✓ Document object is created
✓ DocumentChunker splits the document correctly

==========================================================
"""

from pathlib import Path

from readers.pdf_reader import PDFReader
from readers.document_chunker import DocumentChunker


def main():

    print("=" * 80)
    print("DOCUMENT CHUNKER TEST")
    print("=" * 80)

    # --------------------------------------------------
    # Locate Sample PDF
    # --------------------------------------------------

    sample_folder = Path("samples")

    pdf_files = list(sample_folder.glob("*.pdf"))

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF found inside samples folder."
        )

    pdf_path = pdf_files[0]

    print(f"\nReading PDF : {pdf_path.name}")

    # --------------------------------------------------
    # Read PDF
    # --------------------------------------------------

    reader = PDFReader()

    document = reader.read(pdf_path)

    print("\nDocument Summary")
    print("-" * 40)

    print(f"File Name : {document.file_name}")
    print(f"Pages     : {document.page_count()}")
    print(f"Words     : {document.word_count()}")

    # --------------------------------------------------
    # Create Chunks
    # --------------------------------------------------

    chunker = DocumentChunker()

    chunks = chunker.create_chunks(document)

    print("\n")
    print("=" * 80)
    print(f"TOTAL CHUNKS : {len(chunks)}")
    print("=" * 80)

    for chunk in chunks:

        print("\n")
        print("-" * 80)

        print(f"Chunk ID   : {chunk.chunk_id}")
        print(f"Page Range : {chunk.page_range()}")
        print(f"Words      : {chunk.word_count()}")

        print("\nPreview\n")

        preview = chunk.text[:300]

        print(preview)

        if len(chunk.text) > 300:
            print("...")

    print("\n")
    print("=" * 80)
    print("Chunking Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":

    main()