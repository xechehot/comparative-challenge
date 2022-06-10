from abc import ABC, abstractmethod
from pandas import DataFrame
from dataclasses import dataclass


@dataclass
class MetricResult(object):
    value: object


class Metric(ABC):

    @property
    @abstractmethod
    def metric_name(self) -> str:
        pass

    @abstractmethod
    def calculate(self, data: DataFrame) -> MetricResult:
        pass


class TotalPurchasedAmountMetric(Metric):
    def __init__(self, field_name):
        self.field_name = field_name

    @property
    def metric_name(self) -> str:
        return 'Total purchased amount'

    def calculate(self, data: DataFrame) -> MetricResult:
        return data[self.field_name].sum()


class AvgPurchasedAmountPerPayingUserMetric(Metric):
    def __init__(self, field_name):
        self.field_name = field_name

    @property
    def metric_name(self) -> str:
        return 'Average purchased amount per paying user'

    def calculate(self, data: DataFrame) -> MetricResult:
        return (
            data
            [data[self.field_name] > 0.]
            [self.field_name]
            .mean()
        )

