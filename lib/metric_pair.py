from dataclasses import dataclass
from typing import TypeVar, Generic

from lib.metric import Metric, MetricResult

MetricPairType = TypeVar('MetricPairType', Metric, MetricResult)


@dataclass
class MetricPair(Generic[MetricPairType]):
    yesterday: MetricPairType
    today: MetricPairType

    def calculate(self, data, group_by):
        yesterday = self.yesterday.calculate(data, group_by)
        today = self.today.calculate(data, group_by)
        return MetricPair(yesterday, today)

    @property
    def change_value(self):
        return self.today - self.yesterday

    @property
    def change_percentage(self):
        return self.change_value / self.yesterday

    def __getitem__(self, item):
        yesterday = self.yesterday[item]
        today = self.today[item]
        return MetricPair(yesterday, today)


