import os
from typing import Optional

import functions_framework
import pandas as pd
from cloudevents.http import CloudEvent
from google.cloud import bigquery, storage
from igc_processor.circling import compute_heading_transition, detect_circling
from igc_processor.parser import igc2df


def input_from_gcs(
    bucket_name: str, file_name: str, project: Optional[str] = None
) -> str:
    """
    GCSからファイルをテキスト形式で読み込む
    """
    client = storage.Client(project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()

    return data


def process(data: str) -> pd.DataFrame:
    """
    IGCファイルのテキストデータをデータフレームに加工する
    """
    df = igc2df(data)
    df["heading"] = compute_heading_transition(df["latitude"], df["longitude"])
    df["circling"] = detect_circling(df["heading"])

    return df


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


@functions_framework.cloud_event
def main(cloud_event: CloudEvent) -> None:
    file_name = cloud_event.data["name"]
    bucket_name = cloud_event.data["bucket"]

    project = os.getenv("PROJECT")
    dataset_id = os.environ["DATASET_ID"]
    table_id = os.environ["TABLE_ID"]

    data = input_from_gcs(bucket_name, file_name, project)
    df = process(data)
    output_to_bq(df, dataset_id, table_id, project)
