"""
==========================================================
Enterprise PDF Reader

Purpose
-------
Read PDF documents and convert them into a Document model.

Responsibilities
----------------
✓ Open PDF
✓ Extract clean text
✓ Create Page objects
✓ Create Document object
✓ Preserve page order
✓ Preserve metadata

This class DOES NOT

✗ Call GPT
✗ Extract business parameters
✗ Compare products
✗ Generate reports

==========================================================
"""

from pathlib import Path
import fitz

from models.document import Document
from models.page import Page


class PDFReader:

    # ======================================================
    # Public
    # ======================================================

    def read(self, pdf_path):

        """
        Reads a PDF and returns a Document object.
        """

        pdf = fitz.open(pdf_path)

        document = Document(

            file_name=Path(pdf_path).name,

            file_path=str(pdf_path),

            file_type="PDF"

        )

        try:

            document.metadata = pdf.metadata

            for page_number, pdf_page in enumerate(pdf, start=1):

                text = pdf_page.get_text("text")

                text = self._clean_text(text)

                page = Page(

                    page_number=page_number,

                    text=text

                )

                document.add_page(page)

            return document

        finally:

            pdf.close()

    # ======================================================
    # Private
    # ======================================================

    def _clean_text(self, text):

        if not text:

            return ""

        cleaned_lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:

                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)