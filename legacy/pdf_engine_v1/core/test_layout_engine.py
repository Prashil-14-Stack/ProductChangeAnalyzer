"""
==========================================================
Layout Engine Inspector

Runs the complete layout pipeline and prints
everything discovered in the document.

==========================================================
"""

import glob

from readers.pdf_reader import PDFReader
from legacy.pdf_engine_v1.core.layout.layout_analyzer import LayoutAnalyzer
from legacy.pdf_engine_v1.core.debug.layout_visualizer import LayoutVisualizer


# ==========================================================
# Summary
# ==========================================================

def print_summary(document):

    print("\n")
    print("=" * 100)
    print("DOCUMENT SUMMARY")
    print("=" * 100)

    print(f"Pages      : {len(document.pages)}")
    print(f"Sections   : {len(getattr(document, 'sections', []))}")
    print(f"Tables     : {len(getattr(document, 'tables', []))}")
    print(f"Figures    : {len(getattr(document, 'figures', []))}")
    print(f"Lists      : {len(getattr(document, 'lists', []))}")


# ==========================================================
# Layout Blocks
# ==========================================================

def print_blocks(document):

    print("\n")
    print("=" * 100)
    print("LAYOUT BLOCKS")
    print("=" * 100)

    for page in document.pages:

        print(f"\nPAGE {page.page_number}")
        print("-" * 100)

        for block in page.layout_blocks:

            print(f"[{block.block_type}]")
            print(block.text)
            print(f"BBOX       : {block.bbox}")

            if hasattr(block, "classification_confidence"):
                print(
                    f"CONFIDENCE : {block.classification_confidence}"
                )

            print("-" * 100)


# ==========================================================
# Sections
# ==========================================================

def print_sections(document):

    print("\n")
    print("=" * 100)
    print("DOCUMENT SECTIONS")
    print("=" * 100)

    sections = getattr(document, "sections", [])

    if not sections:

        print("No sections detected.")
        return

    for index, section in enumerate(sections, start=1):

        print(f"\nSECTION {index}")
        print("-" * 100)

        print(f"TITLE      : {section.title}")
        print(f"PAGE       : {section.page_number}")
        print(f"PARAGRAPHS : {len(section.paragraphs)}")
        print(f"TABLES     : {len(section.tables)}")
        print(f"FIGURES    : {len(section.figures)}")

        print()

        print(section.text)

        print("-" * 100)


# ==========================================================
# Tables
# ==========================================================

def print_tables(document):

    print("\n")
    print("=" * 100)
    print("TABLES")
    print("=" * 100)

    tables = getattr(document, "tables", [])

    if not tables:

        print("No tables detected.")
        return

    for index, table in enumerate(tables, start=1):

        print(f"\nTABLE {index}")
        print("-" * 100)

        print(f"PAGE        : {table.page_number}")
        print(f"TABLE ID    : {table.table_id}")
        print(f"ROWS        : {table.row_count}")
        print(f"COLUMNS     : {table.column_count}")
        print(f"CELLS       : {table.cell_count}")
        print(f"BBOX        : {table.bbox}")

        print("\nTABLE CONTENT")
        print("-" * 100)

        for row in table.rows:

            print(

                " | ".join(

                    cell.text.strip()

                    for cell in row.cells

                )

            )

        print("-" * 100)


# ==========================================================
# Figures
# ==========================================================

def print_figures(document):

    print("\n")
    print("=" * 100)
    print("FIGURES")
    print("=" * 100)

    figures = getattr(document, "figures", [])

    if not figures:

        print("No figures detected.")
        return

    for index, figure in enumerate(figures, start=1):

        print(f"\nFIGURE {index}")

        print(f"PAGE : {figure.page_number}")
        print(f"TYPE : {figure.figure_type}")
        print(f"BBOX : {figure.bbox}")


# ==========================================================
# Lists
# ==========================================================

def print_lists(document):

    print("\n")
    print("=" * 100)
    print("LISTS")
    print("=" * 100)

    lists = getattr(document, "lists", [])

    if not lists:

        print("No lists detected.")
        return

    for index, lst in enumerate(lists, start=1):

        print(f"\nLIST {index}")

        print(f"PAGE : {lst.page_number}")
        print(f"ITEMS: {lst.item_count}")

        print(lst.text)


# ==========================================================
# Main
# ==========================================================

def main():

    pdf_files = glob.glob(

        "test_documents/*.pdf"

    )

    if not pdf_files:

        raise FileNotFoundError(

            "No PDF files found inside test_documents."

        )

    pdf_path = pdf_files[0]

    print(f"\nReading : {pdf_path}")

    reader = PDFReader()

    analyzer = LayoutAnalyzer()

    with open(pdf_path, "rb") as file:

        document = reader.read(file)

    # --------------------------------------------------
    # Run Layout Engine
    # --------------------------------------------------

    document = analyzer.analyze(document)

    # --------------------------------------------------
    # Print Results
    # --------------------------------------------------

    print_summary(document)

    print_blocks(document)

    print_sections(document)

    print_tables(document)

    print_figures(document)

    print_lists(document)

    # --------------------------------------------------
    # Visual Debug PDF
    # --------------------------------------------------

    print("\n")
    print("=" * 100)
    print("GENERATING LAYOUT VISUALIZATION")
    print("=" * 100)

    visualizer = LayoutVisualizer()

    visualizer.visualize(

        pdf_path,

        document

    )

    print("\n")
    print("=" * 100)
    print("DONE")
    print("=" * 100)


if __name__ == "__main__":

    main()