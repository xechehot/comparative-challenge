import pytest
from pandas import DataFrame

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
        get_record(2, 1, 1.1, country='Russia'),
        get_record(3, 3.5, 3, country='Russia', is_vip=True),
        get_record(4, 0, 3),
        get_record(5, 0, 0),
        get_record(6, 10, 0),
        get_record(7, 2, 0, country='Russia'),
        get_record(8, 13, 16),
        get_record(9, 0, 1, country='Russia')
    ]
    return DataFrame.from_records(records)


def test_total_amount_metric(default_data):
    metric = TotalPurchasedAmountMetric('purchased_amount_yesterday')
    actual = metric.calculate(default_data)
    expected = 52.5
    assert actual == expected


def test_total_amount_metric_with_group_by(default_data):
    metric = TotalPurchasedAmountMetric('purchased_amount_yesterday')
    actual = metric.calculate(default_data, ['country', 'is_vip'])
    print(actual)
#     TODO add expected value


def test_avg_purchased_amount_per_paying_user_metric(default_data):
    metric = AvgPurchasedAmountPerPayingUserMetric('purchased_amount_yesterday')
    actual = metric.calculate(default_data)
    expected = 8.75
    assert actual == expected


def test_avg_purchased_amount_per_paying_user_metric_with_group_by(default_data):
    metric = AvgPurchasedAmountPerPayingUserMetric('purchased_amount_yesterday')
    actual = metric.calculate(default_data, ['country', 'is_vip'])
    print(actual)
