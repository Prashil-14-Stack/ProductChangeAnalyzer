import fitz

from models.document import Document
from models.document_page import DocumentPage
from models.document_block import DocumentBlock
from models.document_table import DocumentTable


class PDFReaderV2:

    """
    Enterprise PDF Reader

    Responsibility
    ----------------
    Read a PDF while preserving its layout.

    No business logic.
    No parameter extraction.
    """

    # ==========================================================
    # Read PDF
    # ==========================================================

    def read(self, uploaded_file):

        # ------------------------------------------------------
        # Open PDF
        # ------------------------------------------------------

        pdf_bytes = uploaded_file.getvalue()

        pdf_document = fitz.open(

            stream=pdf_bytes,

            filetype="pdf"

        )

        # ------------------------------------------------------
        # Create Enterprise Document
        # ------------------------------------------------------

        document = Document(

            filename=uploaded_file.name,

            file_type="pdf",

            version=1

        )

        # ------------------------------------------------------
        # Read Every Page
        # ------------------------------------------------------

        for page_number, page in enumerate(pdf_document, start=1):

            page_object = DocumentPage(

                page_number=page_number,

                width=page.rect.width,

                height=page.rect.height,

                rotation=page.rotation

            )

            # ==================================================
            # TEXT BLOCKS
            # ==================================================

            blocks = page.get_text("blocks")

            for block in blocks:

                x0, y0, x1, y1, text, block_no, block_type = block

                text = text.strip()

                if not text:

                    continue

                document_block = DocumentBlock(

                    page=page_number,

                    block_number=block_no,

                    block_type=block_type,

                    text=text,

                    bbox=(x0, y0, x1, y1)

                )

                page_object.add_block(

                    document_block

                )

            # ==================================================
            # TABLE EXTRACTION
            # ==================================================

            try:

                table_finder = page.find_tables()

                for index, table in enumerate(

                    table_finder.tables,

                    start=1

                ):

                    document_table = DocumentTable(

                        page=page_number,

                        table_number=index,

                        rows=table.extract()

                    )

                    page_object.add_table(

                        document_table

                    )

            except Exception as e:

                print(

                    f"No tables detected on Page {page_number}: {e}"

                )

            # --------------------------------------------------
            # Add Page to Document
            # --------------------------------------------------

            document.add_page(

                page_object

            )

        pdf_document.close()

        # ------------------------------------------------------
        # Debug
        # ------------------------------------------------------

        self.print_document(

            document

        )

        return document

    # ==========================================================
    # Debug Utility
    # ==========================================================

    def print_document(self, document):

        print("\n" + "=" * 100)

        print("DOCUMENT STRUCTURE")

        print("=" * 100)

        print(f"Filename : {document.filename}")

        print(f"Pages    : {document.page_count}")

        print(f"Blocks   : {document.block_count}")

        print(f"Tables   : {document.table_count}")

        for page in document.pages:

            print("\n" + "-" * 100)

            print(f"PAGE {page.page_number}")

            print(f"Size : {page.width:.2f} x {page.height:.2f}")

            print(f"Rotation : {page.rotation}")

            print(f"Blocks : {page.block_count}")

            print(f"Tables : {page.table_count}")

            print("\nTEXT BLOCKS")

            for block in page.blocks:

                print("-" * 60)

                print(f"Block #{block.block_number}")

                print(block.text)

            if page.tables:

                print("\nTABLES")

                for table in page.tables:

                    print(f"\nTable {table.table_number}")

                    for row in table.rows:

                        print(row)

        print("=" * 100)