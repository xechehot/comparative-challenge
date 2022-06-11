from dataclasses import dataclass
from typing import List

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
               f'({self.change_direction} {self.change_percentage:.2f}% from yesterday {self.metric_pair.yesterday:.2f})'


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

    def combine(self, data: DataFrame, dimension_fields: List[str]):
        result = []
        for metric_pair in self.metric_pairs:
            overall = metric_pair.calculate(data, None)
            result.append(MetricCombinerResult(metric_pair.today.metric_name, overall))
            for dimensions in subslices(dimension_fields):
                segment_name_provider = self.segment_names_provider_factory.get_segment_name_provider(dimensions)
                segment = metric_pair.calculate(data, dimensions)
                condition = self.significant_condition.is_satisfied(overall, segment)
                satisfied_segments = segment[condition]
                segments_result = DataFrame(dict(yesterday=satisfied_segments.yesterday,
                                                 today=satisfied_segments.today))
                for key, row in segments_result.iterrows():
                    payload = MetricCombinerResult(segment_name_provider.get_segment_name(key),
                                                   MetricPair(row.yesterday, row.today))
                    result.append(payload)
        return result
