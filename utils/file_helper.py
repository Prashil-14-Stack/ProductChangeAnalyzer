import os
import shutil

from readers.word_reader import WordReader
from readers.pdf_reader import PDFReader

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
    
    @staticmethod    
    def read_document(uploaded_file):
        """
        Automatically selects the correct reader
        based on the uploaded file extension.
        """

        extension = uploaded_file.name.lower().split(".")[-1]

        if extension == "docx":
            reader = WordReader()
            return reader.read(uploaded_file)

        elif extension == "pdf":
            reader = PDFReader()
            return reader.read(uploaded_file)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )