import pytest
from pandas import DataFrame, Series

from lib.metric import TotalPurchasedAmountMetric, AvgPurchasedAmountPerPayingUserMetric


def get_record(user_id, amount_yesterday, amount_today, country='Canada', is_vip=False):
    return dict(user_id=user_id,
                country=country,
                is_vip=is_vip,
                purchased_amount_yesterday=amount_yesterday,
                purchased_amount_today=amount_today)


@pytest.fixture
def default_data():
    records = [
        get_record(1, 23, 27, is_vip=True),
        get_record(2, 1, 1.1),
        get_record(3, 3.5, 3),
        get_record(4, 0, 3),
        get_record(5, 0, 0),
        get_record(6, 10, 0)
    ]
    return DataFrame.from_records(records)


def test_total_amount_metric(default_data):
    metric = TotalPurchasedAmountMetric('purchased_amount_yesterday')
    actual = metric.calculate(default_data)
    expected = 37.5
    assert actual == expected


def test_avg_purchased_amount_per_paying_user_metric(default_data):
    metric = AvgPurchasedAmountPerPayingUserMetric('purchased_amount_yesterday')
    actual = metric.calculate(default_data)
    expected = 9.375
    assert actual == expected
