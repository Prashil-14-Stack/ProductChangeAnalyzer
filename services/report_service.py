import os
import json
import pandas as pd


SUMMARY_FILE = "outputs/summary.json"
from config.report_config import (
    REPORT_FOLDER,
    REPORT_NAME
)

REPORT_FILE = f"{REPORT_FOLDER}/{REPORT_NAME}"


class ReportService:

    def __init__(self):

        pass

    # =====================================
    # LOAD SUMMARY
    # =====================================

    def get_summary(self):

        default_summary = {

            "parameters_compared": 0,
            "matches_found": 0,
            "new_parameters": 0,
            "review_required": 0,
            "effort_saving": "0%"

        }

        if not os.path.exists(
            SUMMARY_FILE
        ):

            return default_summary

        try:

            with open(
                SUMMARY_FILE,
                "r"
            ) as file:

                summary = json.load(
                    file
                )

            return summary

        except Exception:

            return default_summary

    # =====================================
    # KPI VALUES
    # =====================================

    def get_dashboard_metrics(self):

        summary = self.get_summary()

        return {

            "parameters_compared":

                summary.get(
                    "parameters_compared",
                    0
                ),

            "matches_found":

                summary.get(
                    "matches_found",
                    0
                ),

            "new_parameters":

                summary.get(
                    "new_parameters",
                    0
                ),

            "review_required":

                summary.get(
                    "review_required",
                    0
                ),

            "effort_saving":

                summary.get(
                    "effort_saving",
                    "0%"
                )

        }

    # =====================================
    # LOAD REPORT
    # =====================================

    def get_report_dataframe(self):

        if not os.path.exists(
            REPORT_FILE
        ):

            return pd.DataFrame()

        try:

            return pd.read_excel(
                REPORT_FILE
            )

        except Exception:

            return pd.DataFrame()

    # =====================================
    # TOP RECORDS
    # =====================================

    def get_top_records(

        self,

        rows=5

    ):

        df = self.get_report_dataframe()

        if df.empty:

            return df

        return df.head(rows)

    # =====================================
    # TOTAL RECORDS
    # =====================================

    def total_records(self):

        df = self.get_report_dataframe()

        return len(df)

    # =====================================
    # COLUMN NAMES
    # =====================================

    def get_columns(self):

        df = self.get_report_dataframe()

        if df.empty:

            return []

        return list(df.columns)

    # =====================================
    # REPORT EXISTS
    # =====================================

    def report_exists(self):

        return os.path.exists(
            REPORT_FILE
        )

    # =====================================
    # REPORT SIZE
    # =====================================

    def report_size(self):

        if not self.report_exists():

            return "0 KB"

        size = os.path.getsize(
            REPORT_FILE
        ) / 1024

        return f"{size:.2f} KB"

    # =====================================
    # REPORT DETAILS
    # =====================================

    def get_report_details(self):

        return {

            "file_name":

                REPORT_FILE,

            "exists":

                self.report_exists(),

            "size":

                self.report_size(),

            "records":

                self.total_records(),

            "columns":

                self.get_columns()

        }

    # =====================================
    # SEARCH REPORT
    # =====================================

    def search(

        self,

        keyword

    ):

        df = self.get_report_dataframe()

        if df.empty:

            return df

        keyword = keyword.lower()

        mask = df.astype(

            str

        ).apply(

            lambda column:

            column.str.lower().str.contains(
                keyword
            )

        )

        return df[
            mask.any(axis=1)
        ]