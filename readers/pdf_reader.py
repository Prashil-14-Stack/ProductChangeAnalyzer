import fitz

from models.pdf_document import PDFDocument
from models.pdf_page import PDFPage
from models.layout_block import LayoutBlock
from models.layout_line import LayoutLine
from models.layout_span import LayoutSpan
from legacy.pdf_engine_v1.core.models.raw_span import RawSpan
from legacy.pdf_engine_v1.core.models.raw_line import RawLine

class PDFReader:
    """
    ==========================================================
    Enterprise PDF Reader

    Reads a PDF using PyMuPDF RAWDICT.

    Responsibilities

    ✓ Read PDF
    ✓ Preserve Layout
    ✓ Preserve Font Information
    ✓ Preserve Coordinates
    ✓ Preserve Reading Order

    Does NOT perform

    ✗ OCR
    ✗ Table Detection
    ✗ Business Parameter Detection
    ✗ AI Analysis
    ✗ Semantic Comparison

    ==========================================================
    """

    def read(

        self,

        uploaded_file

    ) -> PDFDocument:

        # ======================================================
        # Open PDF
        # ======================================================

        pdf = fitz.open(

            stream=uploaded_file.read(),

            filetype="pdf"

        )

        # ======================================================
        # Create Document
        # ======================================================

        document = PDFDocument(

            filename=getattr(

                uploaded_file,

                "name",

                "Uploaded PDF"

            )

        )

        # ======================================================
        # Read Every Page
        # ======================================================

        for page_index in range(len(pdf)):

            pdf_page = pdf.load_page(

                page_index

            )

            page = PDFPage(

                page_number=page_index + 1,

                width=pdf_page.rect.width,

                height=pdf_page.rect.height

            )

            # ==================================================
            # Extract RAWDICT
            # ==================================================

            raw = pdf_page.get_text(

                "rawdict"

            )

            # ==================================================
            # Parse Blocks
            # ==================================================

            for block_number, block in enumerate(

                raw.get("blocks", []),

                start=1

            ):

                # Ignore image blocks for now
                if block.get("type") != 0:
                    continue

                layout_block = LayoutBlock(

                    block_number=block_number,

                    page_number=page.page_number,

                    bbox=tuple(

                        block.get(

                            "bbox",

                            (0, 0, 0, 0)

                        )

                    )

                )

                # ==============================================
                # Parse Lines
                # ==============================================

                for line in block.get("lines", []):

                    # --------------------------------------------------
                    # Create Layout Line
                    # --------------------------------------------------

                    layout_line = LayoutLine(

                        bbox=tuple(

                            line.get(

                                "bbox",

                                (0, 0, 0, 0)

                            )

                        ),

                        writing_direction=tuple(

                            line.get(

                                "dir",

                                (1, 0)

                            )

                        )

                    )

                    # --------------------------------------------------
                    # Create Raw Line
                    # --------------------------------------------------

                    raw_line = RawLine(

                        bbox=tuple(

                            line.get(

                                "bbox",

                                (0, 0, 0, 0)

                            )

                        )

                    )

                # ==============================================
                # Parse Lines
                # ==============================================

                for line in block.get("lines", []):

                    # --------------------------------------------------
                    # Create Layout Line
                    # --------------------------------------------------

                    layout_line = LayoutLine(

                        bbox=tuple(

                            line.get(

                                "bbox",

                                (0, 0, 0, 0)

                            )

                        ),

                        writing_direction=tuple(

                            line.get(

                                "dir",

                                (1, 0)

                            )

                        )

                    )

                    # --------------------------------------------------
                    # Create Raw Line
                    # --------------------------------------------------

                    raw_line = RawLine(

                        bbox=tuple(

                            line.get(

                                "bbox",

                                (0, 0, 0, 0)

                            )

                        )

                    )

                    # ==============================================
                    # Parse Spans
                    # ==============================================

                    for span in line.get("spans", []):

                        chars = span.get("chars", [])

                        text = "".join(

                            character.get("c", "")

                            for character in chars

                        )

                        # ------------------------------------------
                        # Existing Layout Span
                        # ------------------------------------------

                        layout_span = LayoutSpan(

                            text=text,

                            bbox=tuple(

                                span.get(

                                    "bbox",

                                    (0, 0, 0, 0)

                                )

                            ),

                            origin=tuple(

                                span.get(

                                    "origin",

                                    (0, 0)

                                )

                            ),

                            font=span.get(

                                "font",

                                ""

                            ),

                            font_size=span.get(

                                "size",

                                0

                            ),

                            flags=span.get(

                                "flags",

                                0

                            ),

                            color=span.get(

                                "color",

                                0

                            )

                        )

                        layout_line.add_span(

                            layout_span

                        )

                        # ------------------------------------------
                        # New Raw Span
                        # ------------------------------------------

                        raw_span = RawSpan(

                            text=text,

                            bbox=tuple(

                                span.get(

                                    "bbox",

                                    (0, 0, 0, 0)

                                )

                            ),

                            origin=tuple(

                                span.get(

                                    "origin",

                                    (0, 0)

                                )

                            ),

                            font=span.get(

                                "font",

                                ""

                            ),

                            font_size=span.get(

                                "size",

                                0

                            ),

                            flags=span.get(

                                "flags",

                                0

                            ),

                            color=span.get(

                                "color",

                                0

                            ),

                            characters=[

                                character.get("c", "")

                                for character in chars

                            ]

                        )

                        raw_line.add_span(

                            raw_span

                        )

                    # --------------------------------------------------
                    # Attach Raw Representation
                    # --------------------------------------------------

                    layout_line.raw_line = raw_line

                    # --------------------------------------------------
                    # Add Completed Line
                    # --------------------------------------------------

                    layout_block.add_line(

                        layout_line

                    )
                page.add_layout_block(

                    layout_block

                )
                print("\n")
                print("=" * 100)
                print(f"BLOCK {layout_block.block_number}")
                print("=" * 100)

                for line in layout_block.lines:

                    print()

                    print(line.raw_line.summary())

                    for span in line.raw_line.spans:

                        print("   ", span.summary())
            # ==================================================
            # Images
            # ==================================================

            for image in pdf_page.get_images(

                full=True

            ):

                page.add_image(

                    {

                        "xref": image[0]

                    }

                )

            # ==================================================
            # Page Metadata
            # ==================================================

            page.metadata = {

                "rotation": pdf_page.rotation,

                "mediabox": (

                    pdf_page.rect.width,

                    pdf_page.rect.height

                )

            }

            document.add_page(

                page

            )

        # ======================================================
        # Document Metadata
        # ======================================================

        document.metadata = {

            "title": pdf.metadata.get(

                "title"

            ),

            "author": pdf.metadata.get(

                "author"

            ),

            "creator": pdf.metadata.get(

                "creator"

            ),

            "producer": pdf.metadata.get(

                "producer"

            ),

            "subject": pdf.metadata.get(

                "subject"

            ),

            "keywords": pdf.metadata.get(

                "keywords"

            )

        }

        document.processing_status = "READ"

        pdf.close()

        return document