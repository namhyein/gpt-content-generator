from datetime import datetime, timezone


def convert_timestamp_to_string(timestamp: int, _format: str = "%d %B %Y") -> str:
    return datetime.fromtimestamp(timestamp).strftime(_format)


def convert_date_to_timestamp(date: datetime = None):
    date = datetime.now() if not date else date
    return int(date.timestamp())


def convert_string_to_datetime(date: str, _format: str = "%Y-%m-%dT%H:%M:%S"):
    return datetime.strptime(date, _format)


def convert_string_to_timestamp(date: str, _format: str = "%Y-%m-%dT%H:%M:%S"):
    date = convert_string_to_datetime(date, _format)
    return convert_date_to_timestamp(date)


def get_now_timestamp():
    """
    returns 10 digits timestamp
    """

    return int(datetime.now(timezone.utc).timestamp())
