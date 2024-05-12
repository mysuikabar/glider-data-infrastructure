import datetime

from amedas_scraper.scraper import get_amedas_data


def test_get_amedas_data():
    get_amedas_data(prec_no="42", block_no="0354", date=datetime.date(2024, 4, 1))
