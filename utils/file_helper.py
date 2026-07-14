import os
import shutil

from models.document import Document

from readers.word_reader import WordReader
from readers.pdf_reader_v2 import PDFReaderV2


class FileHelper:

    @staticmethod
    def create_folder(folder_path):

        from config import UPLOAD_FOLDER

        os.makedirs(

            UPLOAD_FOLDER,

            exist_ok=True

        )

    @staticmethod
    def folder_exists(folder_path):

        return os.path.exists(

            folder_path

        )

    @staticmethod
    def copy_file(source, destination):

        shutil.copy(

            source,

            destination

        )

    @staticmethod
    def delete_file(file_path):

        if os.path.exists(file_path):

            os.remove(file_path)

    @staticmethod
    def delete_folder(folder_path):

        if os.path.exists(folder_path):

            shutil.rmtree(folder_path)

    @staticmethod
    def file_size(file_path):

        if not os.path.exists(file_path):

            return 0

        return round(

            os.path.getsize(file_path) / 1024,

            2

        )

    @staticmethod
    def list_files(folder_path):

        if not os.path.exists(folder_path):

            return []

        return sorted(

            os.listdir(folder_path)

        )

    # ==========================================================
    # Read Document
    # ==========================================================

    @staticmethod
    def read_document(

        uploaded_file

    ) -> Document:

        """
        Automatically selects the correct reader
        and returns a canonical Document object.
        """

        _, extension = os.path.splitext(uploaded_file.name.lower())
        extension = extension.lstrip(".")

        # ------------------------------------------------------
        # Microsoft Word
        # ------------------------------------------------------

        if extension == "docx":

            reader = WordReader()

            return reader.read(

                uploaded_file

            )

        # ------------------------------------------------------
        # PDF
        # ------------------------------------------------------

        elif extension == "pdf":

            reader = PDFReaderV2()

            return reader.read(

                uploaded_file

            )

        # ------------------------------------------------------
        # Unsupported
        # ------------------------------------------------------

        raise ValueError(

            f"Unsupported file type: {extension}"

        )