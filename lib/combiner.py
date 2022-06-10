from typing import List

from pandas import DataFrame

from lib.metric import Metric
from lib.metric_pair import MetricPair
from lib.significant_condition import SignificantCondition
from lib.utils import subslices


class MetricCombiner(object):
    def __init__(self, metric_pairs: List[MetricPair],
                 significant_condition: SignificantCondition):
        self.metric_pairs = metric_pairs
        self.significant_condition = significant_condition

    @staticmethod
    def _calculate_metric(data: DataFrame, metric: Metric, group_by=None):
        return metric.calculate(data, group_by)

    def combine(self, data: DataFrame, dimension_fields: List[str]):
        overalls = [pair.calculate(data, None) for pair in self.metric_pairs]
        for dimensions in subslices(dimension_fields):
            for overall, pair in zip(overalls, self.metric_pairs):
                segment = pair.calculate(data, dimensions)
                if self.significant_condition.is_satisfied(overall, segment):
                    # TODO add to result here
                    pass
