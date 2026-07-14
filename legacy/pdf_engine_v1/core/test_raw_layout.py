"""
==========================================================
PyMuPDF RAW Layout Inspector

Purpose
-------
Inspect the RAW structure extracted by PyMuPDF.

Hierarchy

Page
    Block
        Line
            Span
                Characters

This script reconstructs span text from characters,
because recent versions of PyMuPDF do not provide
span["text"].

==========================================================
"""

import fitz
import glob


# ==========================================================
# Reconstruct Span Text
# ==========================================================

def get_span_text(span):

    chars = span.get("chars", [])

    return "".join(

        ch.get("c", "")

        for ch in chars

    )


# ==========================================================
# Inspect PDF
# ==========================================================

def inspect_pdf(pdf_path):

    print("=" * 120)
    print("RAW PDF LAYOUT INSPECTOR")
    print("=" * 120)

    doc = fitz.open(pdf_path)

    for page_index, page in enumerate(doc):

        raw = page.get_text("rawdict")

        print("\n")
        print("=" * 120)
        print(f"PAGE {page_index + 1}")
        print("=" * 120)

        blocks = raw.get("blocks", [])

        print(f"Total Blocks : {len(blocks)}")

        # --------------------------------------------------

        for block_number, block in enumerate(blocks):

            if block.get("type") != 0:
                continue

            print("\n")
            print("-" * 120)
            print(f"BLOCK {block_number}")
            print("-" * 120)

            print(f"BBOX : {block.get('bbox')}")

            lines = block.get("lines", [])

            print(f"LINES : {len(lines)}")

            # --------------------------------------------------

            for line_number, line in enumerate(lines):

                print()

                print(f"LINE {line_number}")

                print(f"BBOX : {line.get('bbox')}")

                spans = line.get("spans", [])

                print(f"SPANS : {len(spans)}")

                # --------------------------------------------------

                for span_number, span in enumerate(spans):

                    text = get_span_text(span)

                    print()

                    print(f"SPAN {span_number}")

                    print(f"TEXT      : {repr(text)}")

                    print(f"FONT      : {span.get('font')}")

                    print(f"SIZE      : {span.get('size')}")

                    print(f"FLAGS     : {span.get('flags')}")

                    print(f"COLOR     : {span.get('color')}")

                    print(f"BBOX      : {span.get('bbox')}")

                    print(f"ORIGIN    : {span.get('origin')}")

                    chars = span.get("chars", [])

                    print(f"CHAR COUNT: {len(chars)}")

                    print("-" * 60)

    doc.close()


# ==========================================================
# Main
# ==========================================================

def main():

    pdf_files = glob.glob(

        "test_documents/*.pdf"

    )

    if not pdf_files:

        raise FileNotFoundError(

            "No PDF found inside test_documents."

        )

    pdf_path = pdf_files[0]

    print(f"\nReading : {pdf_path}")

    inspect_pdf(pdf_path)


# ==========================================================

if __name__ == "__main__":

    main()