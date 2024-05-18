import datetime
import os
from typing import Optional

import flask
import functions_framework
import pandas as pd
from amedas_scraper.scraper import get_amedas_data
from google.cloud import bigquery

# point code
PREC_NO = "42"  # 群馬県
BLOCK_NO = "0354"  # 館林


def output_to_bq(
    df: pd.DataFrame, dataset_id: str, table_id: str, project: Optional[str] = None
) -> None:
    """
    データフレームをBigQueryの指定したテーブルに追加する
    """
    client = bigquery.Client(project)
    table = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True  # TODO: スキーマを定義したい
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    job = client.load_table_from_dataframe(df, table, job_config=job_config)
    job.result()

    return


@functions_framework.http
def main(request: flask.Request) -> str:
    project = os.getenv("PROJECT")
    dataset_id = os.environ["DATASET_ID"]
    table_id = os.environ["TABLE_ID"]

    date = datetime.date.today() - datetime.timedelta(days=2)
    df = get_amedas_data(prec_no=PREC_NO, block_no=BLOCK_NO, date=date)
    output_to_bq(df, dataset_id=dataset_id, table_id=table_id, project=project)

    return "Success"
