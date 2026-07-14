"""
==========================================================
Reader Factory

Purpose
-------
Returns the appropriate document reader based
on the uploaded file type.

Responsibilities
----------------
✓ Detect file extension
✓ Return correct reader
✓ Hide reader selection from the application

Supported Formats
-----------------
✓ PDF
✓ DOCX

Future
------
✓ DOC
✓ TXT
✓ HTML

==========================================================
"""

from pathlib import Path

from v2.readers.pdf_reader import PDFReader

# Import when WordReader is available
# from readers.word_reader import WordReader


class ReaderFactory:

    # ======================================================
    # Public
    # ======================================================

    @staticmethod
    def get_reader(file_path):

        extension = Path(file_path).suffix.lower()

        # --------------------------------------------------
        # PDF
        # --------------------------------------------------

        if extension == ".pdf":

            return PDFReader()

        # --------------------------------------------------
        # Word
        # --------------------------------------------------

        elif extension in [

            ".docx",

            ".doc"

        ]:

            # return WordReader()

            raise NotImplementedError(

                "WordReader is not implemented yet."

            )

        # --------------------------------------------------
        # Unsupported
        # --------------------------------------------------

        raise ValueError(

            f"Unsupported file format: {extension}"

        )