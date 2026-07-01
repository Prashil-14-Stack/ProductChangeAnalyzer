import pandas as pd


class ExcelHelper:

    @staticmethod
    def read_excel(file_path):

        try:

            return pd.read_excel(
                file_path
            )

        except Exception:

            return pd.DataFrame()

    @staticmethod
    def top_rows(df, rows=5):

        if df.empty:

            return df

        return df.head(rows)

    @staticmethod
    def total_rows(df):

        return len(df)

    @staticmethod
    def columns(df):

        return list(df.columns)

    @staticmethod
    def is_empty(df):

        return df.empty