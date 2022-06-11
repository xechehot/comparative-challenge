from enum import Enum
from typing import Union

import pytest
from pandas import DataFrame, Series, MultiIndex
from pandas.testing import assert_series_equal
from pandas.core.groupby import DataFrameGroupBy

from lib.metric import Metric, MetricResult
from lib.metric_pair import MetricPair


class FakeMetricType(Enum):
    yesterday = 'yesterday'
    today = 'today'


fake_metric_type_expected_values = {
    FakeMetricType.yesterday: 3,
    FakeMetricType.today: 4
}


class FakeMetric(Metric):
    def __init__(self, metric_type: FakeMetricType):
        self.metric_type = metric_type

    @property
    def metric_name(self) -> str:
        return 'Fake metric'

    @property
    def metric_id(self) -> str:
        return 'fake_metric'

    def _calculate(self, data: Union[DataFrame, DataFrameGroupBy]) -> MetricResult:
        return fake_metric_type_expected_values.get(self.metric_type)


@pytest.fixture
def fake_metric_yesterday():
    return FakeMetric(FakeMetricType.yesterday)


@pytest.fixture
def fake_metric_today():
    return FakeMetric(FakeMetricType.today)


@pytest.fixture
def fake_data():
    return DataFrame.from_records([{'country': 'Canada'}])


def test_metric_pair_calculate(fake_data, fake_metric_yesterday, fake_metric_today):
    expected_yesterday = fake_metric_type_expected_values[FakeMetricType.yesterday]
    expected_today = fake_metric_type_expected_values[FakeMetricType.today]
    assert fake_metric_yesterday.calculate(fake_data, None) == expected_yesterday
    assert fake_metric_today.calculate(fake_data, None) == expected_today

    pair = MetricPair(fake_metric_yesterday, fake_metric_today)
    result = pair.calculate(fake_data, None)

    assert result.yesterday == expected_yesterday
    assert result.today == expected_today


def get_series_result(data, name):
    index = MultiIndex.from_product([['Canada', 'Russia'], [False, True]],
                                    names=['country', 'is_vip'])
    return Series(data,
                  index=index,
                  name=name)


@pytest.fixture
def yesterday_series_result():
    return get_series_result([10., 5, 4, 1.], 'purchased_amount_yesterday')


@pytest.fixture
def today_series_result():
    return get_series_result([12., 4, 4, 2.], 'purchased_amount_today')


def test_metric_pair_change_value_series(yesterday_series_result, today_series_result):
    pair = MetricPair(yesterday_series_result, today_series_result)
    expected = get_series_result([2., -1, 0, 1], None)
    assert_series_equal(pair.change_value, expected)


def test_metric_pair_change_value_series_int(yesterday_series_result):
    pair = MetricPair(yesterday_series_result, 20.)
    expected = get_series_result([10.0, 15.0, 16.0, 19.0], 'purchased_amount_yesterday')
    assert_series_equal(pair.change_value, expected)

    pair = MetricPair(20., yesterday_series_result)
    expected = get_series_result([-10.0, -15.0, -16.0, -19.0], 'purchased_amount_yesterday')
    assert_series_equal(pair.change_value, expected)


def test_metric_pair_change_percentage_series(yesterday_series_result, today_series_result):
    pair = MetricPair(yesterday_series_result, today_series_result)
    expected = get_series_result([0.2, -0.2, 0, 1], None)
    assert_series_equal(pair.change_percentage, expected)


def test_metric_pair_change_percentage_series_int(yesterday_series_result):
    pair = MetricPair(yesterday_series_result, 20.)
    expected = get_series_result([1.0, 3.0, 4.0, 19.0], 'purchased_amount_yesterday')
    assert_series_equal(pair.change_percentage, expected)

    pair = MetricPair(20., yesterday_series_result)
    expected = get_series_result([-0.5, -0.75, -0.8, -0.95], 'purchased_amount_yesterday')
    assert_series_equal(pair.change_percentage, expected)


def test_metric_pair_change_value_int():
    pair = MetricPair(10, 15)
    assert pair.change_value == 5


def test_metric_pair_change_percentage_int():
    pair = MetricPair(10, 15)
    assert pair.change_percentage == 0.5
