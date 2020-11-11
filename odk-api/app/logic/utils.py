from datetime import datetime
from typing import Union

DATE_FMT = "%Y-%m-%d"
ACCEPTED_INPUT_FMTS = (
    f"{DATE_FMT} %H:%M:%S.%f",
    f"{DATE_FMT} %H.%M.%S.%f",
    f"{DATE_FMT}T%H.%M.%S.%f"
)
OUTPUT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def translate_datetime_string(date_str) -> datetime:
    for fmt in ACCEPTED_INPUT_FMTS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Invalid date format: {date_str}")


def correct_date_string(date: Union[str, datetime]) -> str:
    try:
        if type(date) == str:
            date = translate_datetime_string(date)
        return datetime.strftime(date, OUTPUT_FORMAT)
    except Exception as e:
        raise e