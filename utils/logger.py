import logging
import os


class Logger:

    @staticmethod
    def get_logger():

        from config import UPLOAD_FOLDER

        os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
        )       

        logging.basicConfig(

            filename="logs/application.log",

            level=logging.INFO,

            format="%(asctime)s | %(levelname)s | %(message)s"

        )

        return logging