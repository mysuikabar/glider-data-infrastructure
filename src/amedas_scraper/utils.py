import datetime
import re


def direction_to_angle(direction: str) -> float:
    """
    16方位を角度に変換する
    """
    directions = {
        "北": 0,
        "北北東": 22.5,
        "北東": 45,
        "東北東": 67.5,
        "東": 90,
        "東南東": 112.5,
        "南東": 135,
        "南南東": 157.5,
        "南": 180,
        "南南西": 202.5,
        "南西": 225,
        "西南西": 247.5,
        "西": 270,
        "西北西": 292.5,
        "北西": 315,
        "北北西": 337.5,
    }
    return directions.get(direction, 0)  # 16方位以外は0に割り当てる（ex. 静穏）


def str_to_datetime(datetime_str: str) -> datetime.datetime:
    """
    yyyy-mm-dd HH:MM という形式のデータをdatetime型に変換する
    2024-01-01 24:00 は 2024-01-02 00:00 として変換する
    """
    pattern = r"(\d+)-(\d+)-(\d+) (\d+):(\d+)"
    result = re.match(pattern, datetime_str)
    if result is None:
        raise ValueError

    year = int(result.group(1))
    month = int(result.group(2))
    day = int(result.group(3))
    hour = int(result.group(4))
    minute = int(result.group(5))

    date = datetime.date(year, month, day)
    if hour != 24:
        time = datetime.time(hour, minute)
    else:
        time = datetime.time(0, minute)
        date = date + datetime.timedelta(days=1)

    return datetime.datetime.combine(date, time)
