from datetime import datetime
from dateutil import tz


def unix2datetime(unixtime) -> datetime:
    return datetime.utcfromtimestamp(unixtime)


def convert_datetime(datetime, str_tz) -> datetime:
    to_zone = tz.gettz(str_tz)
    result = datetime.astimezone(to_zone)
    return result
