from lib.combiner import MetricCombinerResult
from lib.metric_pair import MetricPair


def test_metric_combiner_result_up_print():
    metric_pair = MetricPair(80., 103.)
    result = MetricCombinerResult('Users from Canada', metric_pair, ('canada',))
    assert str(result) == 'Users from Canada: $103.00 (up 28.75% from yesterday)'


def test_metric_combiner_result_down_print():
    metric_pair = MetricPair(103., 80)
    result = MetricCombinerResult('Users from Canada', metric_pair, ('canada',))
    print(result)
    assert str(result) == 'Users from Canada: $80.00 (down 22.33% from yesterday)'


def test_sort_metric_combiner_result_by_index():
    metric_indexes = [[0, 'canada', True],
                      [0, 'canada'],
                      [1, False],
                      [0, 'canada', False],
                      [1, True]]
    pair = MetricPair(1., 2.)
    metric_pairs = [MetricCombinerResult(str(index), pair, index) for index in metric_indexes]
    metric_pairs.sort(key=lambda x: x.index)
    actual_indexes = [r.index for r in metric_pairs]
    expected_indexes = [[0, 'canada'],
                        [0, 'canada', False],
                        [0, 'canada', True],
                        [1, False],
                        [1, True]]
    assert actual_indexes == expected_indexes
