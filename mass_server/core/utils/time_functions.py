from datetime import datetime
from pytz import utc


class TimeFunctions:
    @staticmethod
    def get_timestamp():
        # We remove the microsecond part of the timestamp here since mongoengine can not handle it correctly and test cases fail due to the lost precision
        return datetime.now(utc).replace(microsecond=0)