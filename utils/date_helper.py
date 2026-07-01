from datetime import datetime


class DateHelper:

    @staticmethod
    def current_timestamp():

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    @staticmethod
    def current_datetime():

        return datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )

    @staticmethod
    def format_datetime(timestamp):

        return datetime.fromtimestamp(
            timestamp
        ).strftime(
            "%d-%b-%Y %H:%M"
        )