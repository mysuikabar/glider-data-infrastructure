import datetime
from collections import defaultdict

import numpy as np
import pandas as pd
import pandera as pa
import requests
from bs4 import BeautifulSoup
from pandera.typing import DataFrame

from .consts import NULL_VALUES
from .schema import AmedasSchema
from .utils import direction_to_angle, str_to_datetime


def _parse_html_to_df(html_txt: str) -> pd.DataFrame:
    """
    アメダスで取得したHTMLをデータフレームに変換する
    """
    soup = BeautifulSoup(html_txt, "html.parser")

    rows = soup.find_all(name="tr", attrs={"class": "mtx"})
    rows = rows[3:]  # ヘッダーを削除

    columns = [
        "timestamp",
        "rainfall",
        "temperature",
        "humidity",
        "wind_speed",
        "wind_direction",
        "wind_speed_max",
        "wind_direction_max",
        "daylight_hours",
    ]

    data = defaultdict(list)
    for row in rows:
        row = row.find_all("td")
        for i, col in enumerate(columns):
            data[col].append(row[i].text)

    return pd.DataFrame(data)


@pa.check_types
def _process_data(df: pd.DataFrame, date: datetime.date) -> DataFrame[AmedasSchema]:
    """
    パースしたデータフレームを前処理する
    """
    df_ = df.copy()

    for value in NULL_VALUES:
        df_ = df_.replace(value, np.nan)

    df_["timestamp"] = str(date) + " " + df_["timestamp"]
    df_["timestamp"] = df_["timestamp"].apply(str_to_datetime)

    df_["wind_direction"] = df_["wind_direction"].map(direction_to_angle)
    df_["wind_direction_max"] = df_["wind_direction_max"].map(direction_to_angle)
    df_["daylight_hours"] = df_["daylight_hours"].fillna(0.0)

    numeric_columns = [col for col in df_.columns if col != "timestamp"]
    df_[numeric_columns] = df_[numeric_columns].astype(float)

    return df_


def get_amedas_data(prec_no: str, block_no: str, date: datetime.date) -> pd.DataFrame:
    """
    指定した地点、時刻のアメダスデータをデータフレームとして取得する

    地点コードはリンク参照: http://k-ichikawa.blog.enjoy.jp/etc/HP/htm/jmaP0.html
    """
    url_template = "https://www.data.jma.go.jp/obd/stats/etrn/view/10min_a1.php?prec_no={prec_no}&block_no={block_no}&year={year}&month={month}&day=1&view="
    url = url_template.format(
        prec_no=prec_no,
        block_no=block_no,
        year=date.year,
        month=date.month,
        day=date.day,
    )
    response = requests.get(url)
    response.encoding = "utf-8"

    df = _parse_html_to_df(response.text)
    df = _process_data(df, date=date)

    return df
