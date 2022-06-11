from lib.combiner import MetricCombinerResult
from lib.metric_pair import MetricPair


def test_metric_combiner_result_up_print():
    metric_pair = MetricPair(80., 103.)
    result = MetricCombinerResult('Users from Canada', metric_pair)
    assert str(result) == 'Users from Canada: $103.00 (up 28.75% from yesterday)'


def test_metric_combiner_result_down_print():
    metric_pair = MetricPair(103., 80)
    result = MetricCombinerResult('Users from Canada', metric_pair)
    print(result)
    assert str(result) == 'Users from Canada: $80.00 (down 22.33% from yesterday)'
