from readers.pdf_reader import PDFReader
import glob
import os

def test_pdf_reader(pdf_path):

    reader = PDFReader()

    with open(pdf_path, "rb") as file:

        document = reader.read(file)

    print("\n" + "=" * 80)

    print("PDF DOCUMENT SUMMARY")

    print("=" * 80)

    print(document.summary())

    print("\n")

    for page in document.pages:

        print("-" * 80)

        print(page.summary())

        print("-" * 80)

        print(f"\nShowing first {min(5, len(page.blocks))} blocks\n")

        for block in page.blocks[:5]:

            print("=" * 60)

            print(f"Block #{block.block_number}")

            print(f"Bounding Box : {block.bbox}")

            print()

            print(block.text)

            print("=" * 60)

        print("=" * 80)

if __name__ == "__main__":

    pdf_file = os.path.join(
        os.getcwd(),
        "test_documents",
        "sample.pdf"
    )

    print(pdf_file)

    test_pdf_reader(pdf_file)