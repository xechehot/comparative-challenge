from dataclasses import dataclass
from typing import List, Tuple, Union

from pandas import DataFrame

from lib.metric import Metric
from lib.metric_pair import MetricPair
from lib.segment_name_provider_factory import SegmentNameProviderFactory
from lib.significant_condition import SignificantCondition
from lib.utils import subslices


@dataclass
class MetricCombinerResult:
    metric_name: str
    metric_pair: MetricPair
    index: Union[List, Tuple]

    @property
    def change_direction(self):
        if self.metric_pair.today > self.metric_pair.yesterday:
            return 'up'
        return 'down'

    @property
    def change_percentage(self):
        return abs(self.metric_pair.change_percentage) * 100

    def __str__(self):
        return f'{self.metric_name}: ${self.metric_pair.today:.2f} ' \
               f'({self.change_direction} {self.change_percentage:.2f}% from yesterday)'


class MetricCombiner(object):
    def __init__(self, metric_pairs: List[MetricPair],
                 significant_condition: SignificantCondition,
                 segment_names_provider_factory: SegmentNameProviderFactory):
        self.metric_pairs = metric_pairs
        self.significant_condition = significant_condition
        self.segment_names_provider_factory = segment_names_provider_factory

    @staticmethod
    def _calculate_metric(data: DataFrame, metric: Metric, group_by=None):
        return metric.calculate(data, group_by)

    @staticmethod
    def get_index(key, i):
        if type(key) not in [tuple, list]:
            key_tuple = (key,)
        else:
            key_tuple = key
        return (i,) + key_tuple

    def combine(self, data: DataFrame, dimension_fields: List[str]):
        result: List[MetricCombinerResult] = []
        for metric_pair in self.metric_pairs:
            overall = metric_pair.calculate(data, None)
            result.append(MetricCombinerResult(metric_pair.today.metric_name, overall, [metric_pair.today.metric_id]))
            dimensions_result: List[MetricCombinerResult] = []
            for i, dimensions in subslices(dimension_fields):
                significant_segments = self.get_significant_segments(metric_pair, data, dimensions, overall)
                for payload in self.get_segment_results(significant_segments, dimensions, i):
                    dimensions_result.append(payload)
            dimensions_result.sort(key=lambda x: x.index)
            result += dimensions_result
        return result

    def get_segment_results(self, significant_segments, dimensions, i):
        segment_name_provider = self.segment_names_provider_factory.get_segment_name_provider(dimensions)
        for key, row in significant_segments.iterrows():
            payload = MetricCombinerResult(segment_name_provider.get_segment_name(key),
                                           MetricPair(row.yesterday, row.today),
                                           self.get_index(key, i))
            yield payload

    def get_significant_segments(self, metric_pair, data, dimensions, overall):
        segment = metric_pair.calculate(data, dimensions)
        condition = self.significant_condition.is_satisfied(overall, segment)
        satisfied_segments = segment[condition]
        return DataFrame(dict(yesterday=satisfied_segments.yesterday,
                              today=satisfied_segments.today))
