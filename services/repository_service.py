import os
from datetime import datetime


BUCKET_FOLDER = "bucket"


class RepositoryService:

    def __init__(self):

        from config import UPLOAD_FOLDER

        os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
        )

    # =====================================
    # GET ALL ANALYSIS RUNS
    # =====================================

    def get_analysis_runs(self):

        analysis_runs = []

        folders = sorted(
            os.listdir(BUCKET_FOLDER),
            reverse=True
        )

        for folder in folders:

            folder_path = os.path.join(
                BUCKET_FOLDER,
                folder
            )

            if not os.path.isdir(
                folder_path
            ):
                continue

            created_time = datetime.fromtimestamp(
                os.path.getctime(
                    folder_path
                )
            )

            files = []

            for file_name in sorted(
                os.listdir(folder_path)
            ):

                file_path = os.path.join(
                    folder_path,
                    file_name
                )

                file_size = round(
                    os.path.getsize(file_path) / 1024,
                    2
                )

                files.append(

                    {

                        "name": file_name,

                        "path": file_path,

                        "size": file_size

                    }

                )

            analysis_runs.append(

                {

                    "analysis_name": folder,

                    "folder_path": folder_path,

                    "created_date": created_time.strftime(
                        "%d-%b-%Y %H:%M"
                    ),

                    "status": "Completed",

                    "file_count": len(files),

                    "files": files

                }

            )

        return analysis_runs

    # =====================================
    # TOTAL ANALYSIS COUNT
    # =====================================

    def get_total_analysis(self):

        count = 0

        folders = os.listdir(
            BUCKET_FOLDER
        )

        for folder in folders:

            if os.path.isdir(

                os.path.join(
                    BUCKET_FOLDER,
                    folder
                )

            ):

                count += 1

        return count

    # =====================================
    # GET LATEST ANALYSIS
    # =====================================

    def get_latest_analysis(self):

        analysis = self.get_analysis_runs()

        if len(
            analysis
        ) == 0:

            return None

        return analysis[0]

    # =====================================
    # SEARCH ANALYSIS
    # =====================================

    def search_analysis(

        self,

        keyword

    ):

        results = []

        for run in self.get_analysis_runs():

            if keyword.lower() in run[
                "analysis_name"
            ].lower():

                results.append(
                    run
                )

        return results

    # =====================================
    # GET FILES
    # =====================================

    def get_files(

        self,

        analysis_name

    ):

        folder_path = os.path.join(

            BUCKET_FOLDER,

            analysis_name

        )

        if not os.path.exists(
            folder_path
        ):

            return []

        files = []

        for file_name in os.listdir(
            folder_path
        ):

            files.append(

                {

                    "name": file_name,

                    "path": os.path.join(
                        folder_path,
                        file_name
                    )

                }

            )

        return files