import pytest
from pandas import MultiIndex, Series
from pandas.testing import assert_series_equal

from lib.metric_pair import MetricPair
from lib.significant_condition import SignificantCondition, AndSignificantCondition, \
    ChangeAbsolutePercentageSignificantCondition, ChangeAbsoluteValueSignificantCondition


class ConstantSignificantCondition(SignificantCondition):
    def __init__(self, condition):
        self.condition = condition

    def is_satisfied(self, overall: MetricPair, segment: MetricPair):
        return self.condition


@pytest.fixture
def true_condition():
    return ConstantSignificantCondition(True)


@pytest.fixture
def false_condition():
    return ConstantSignificantCondition(False)


@pytest.fixture
def and_significant_test_cases(false_condition, true_condition):
    return [
        [False, [false_condition, true_condition]],
        [False, [true_condition, false_condition]],
        [False, [false_condition, false_condition]],
        [True, [true_condition, true_condition]],
        [False, [true_condition, true_condition, false_condition]],
    ]


def test_and_significant_condition(and_significant_test_cases):
    for expected, conditions in and_significant_test_cases:
        target_condition = AndSignificantCondition(conditions)
        assert target_condition.is_satisfied(None, None) == expected


def get_series_result(data, name):
    index = MultiIndex.from_product([['Canada', 'Russia'], [False, True]],
                                    names=['country', 'is_vip'])
    return Series(data,
                  index=index,
                  name=name)


def test_change_absolute_percentage_condition_int():
    target_condition = ChangeAbsolutePercentageSignificantCondition(0.02)
    overall = MetricPair(10, 12)
    print(overall.change_percentage)

    significant_segment = MetricPair(1., 1.5)
    assert target_condition.is_satisfied(overall, significant_segment) is True

    insignificant_segment = MetricPair(10., 12.1)
    print(insignificant_segment.change_percentage)
    assert target_condition.is_satisfied(overall, insignificant_segment) is False


@pytest.fixture
def overall():
    return MetricPair(42.5, 49.8)


@pytest.fixture
def yesterday_segment():
    return get_series_result([23, 1, 3.5, 15], 'purchased_amount_yesterday')


@pytest.fixture
def today_segment():
    return get_series_result([27, 1.1, 3, 18.7], 'purchased_amount_today')


def test_change_absolute_percentage_condition_series(overall, yesterday_segment, today_segment):
    target_condition = ChangeAbsolutePercentageSignificantCondition(0.02)
    segment = MetricPair(yesterday_segment, today_segment)
    expected = get_series_result([False, False, False, True], None)
    assert_series_equal(target_condition.is_satisfied(overall, segment), expected)


def test_change_absolute_value_condition_series(overall, yesterday_segment, today_segment):
    target_condition = ChangeAbsoluteValueSignificantCondition(0.02)
    segment = MetricPair(yesterday_segment, today_segment)
    expected = get_series_result([True, False, True, True], None)
    assert_series_equal(target_condition.is_satisfied(overall, segment), expected)


def test_absolute_percentage_and_absolute_value_condition_series(overall, yesterday_segment, today_segment):
    absolute_percentage_condition = ChangeAbsolutePercentageSignificantCondition(0.02)
    absolute_value_condition = ChangeAbsoluteValueSignificantCondition(0.02)
    target_condition = AndSignificantCondition([absolute_percentage_condition, absolute_value_condition])

    segment = MetricPair(yesterday_segment, today_segment)
    expected = get_series_result([False, False, False, True], None)
    assert_series_equal(target_condition.is_satisfied(overall, segment), expected)
