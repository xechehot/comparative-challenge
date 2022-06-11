from enum import Enum
from typing import Union

import pytest
from pandas import DataFrame
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
