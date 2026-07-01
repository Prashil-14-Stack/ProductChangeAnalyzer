import os
from datetime import datetime


BUCKET_FOLDER = "bucket"


class HistoryService:

    def __init__(self):

        from config import UPLOAD_FOLDER

        os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
        )

    # =====================================
    # GET COMPLETE HISTORY
    # =====================================

    def get_history(self):

        history = []

        analysis_runs = sorted(
            os.listdir(BUCKET_FOLDER),
            reverse=True
        )

        serial_number = 1

        for run in analysis_runs:

            folder_path = os.path.join(
                BUCKET_FOLDER,
                run
            )

            if not os.path.isdir(folder_path):
                continue

            created_time = datetime.fromtimestamp(
                os.path.getctime(folder_path)
            )

            files = os.listdir(folder_path)

            history.append(

                {

                    "serial_no": serial_number,

                    "analysis_id": run,

                    "user": "Prashil Wanjari",

                    "date": created_time.strftime(
                        "%d-%b-%Y %H:%M"
                    ),

                    "status": "Completed",

                    "total_files": len(files),

                    "folder_path": folder_path

                }

            )

            serial_number += 1

        return history

    # =====================================
    # TOTAL ANALYSIS
    # =====================================

    def total_analysis(self):

        return len(
            self.get_history()
        )

    # =====================================
    # LATEST ANALYSIS
    # =====================================

    def latest_analysis(self):

        history = self.get_history()

        if len(history) == 0:

            return None

        return history[0]

    # =====================================
    # SEARCH ANALYSIS
    # =====================================

    def search_analysis(

        self,

        keyword

    ):

        results = []

        keyword = keyword.lower()

        for analysis in self.get_history():

            if (

                keyword
                in
                analysis["analysis_id"].lower()

            ):

                results.append(
                    analysis
                )

        return results

    # =====================================
    # FILTER BY STATUS
    # =====================================

    def filter_by_status(

        self,

        status

    ):

        results = []

        for analysis in self.get_history():

            if (

                analysis["status"]

                ==

                status

            ):

                results.append(
                    analysis
                )

        return results

    # =====================================
    # GET ANALYSIS DETAILS
    # =====================================

    def get_analysis_details(

        self,

        analysis_id

    ):

        for analysis in self.get_history():

            if (

                analysis["analysis_id"]

                ==

                analysis_id

            ):

                return analysis

        return None

    # =====================================
    # DELETE ANALYSIS
    # =====================================

    def delete_analysis(

        self,

        analysis_id

    ):

        folder_path = os.path.join(

            BUCKET_FOLDER,

            analysis_id

        )

        if os.path.exists(
            folder_path
        ):

            import shutil

            shutil.rmtree(
                folder_path
            )

            return True

        return False