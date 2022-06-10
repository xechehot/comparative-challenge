from abc import ABC, abstractmethod
from pandas import DataFrame
from dataclasses import dataclass
from typing import Union
from pandas.core.groupby import DataFrameGroupBy


@dataclass
class MetricResult(object):
    value: object


class Metric(ABC):
    @property
    @abstractmethod
    def metric_name(self) -> str:
        pass

    @abstractmethod
    def _calculate(self, data: Union[DataFrame, DataFrameGroupBy]) -> MetricResult:
        pass

    def calculate(self, data: DataFrame, group_by=None) -> MetricResult:
        if group_by is not None:
            return self._calculate(data.groupby(by=group_by))
        return self._calculate(data)


class TotalPurchasedAmountMetric(Metric):
    def __init__(self, field_name):
        self.field_name = field_name

    @property
    def metric_name(self) -> str:
        return 'Total purchased amount'

    def _calculate(self, data: Union[DataFrame, DataFrameGroupBy]) -> MetricResult:
        return data[self.field_name].sum()


class AvgPurchasedAmountPerPayingUserMetric(Metric):
    def __init__(self, field_name):
        self.field_name = field_name

    @property
    def metric_name(self) -> str:
        return 'Average purchased amount per paying user'

    def _calculate(self, data: Union[DataFrame, DataFrameGroupBy]) -> MetricResult:
        return data[self.field_name].mean()

    def calculate(self, data: DataFrame, group_by=None) -> MetricResult:
        filtered_data = data[data[self.field_name] > 0]
        return super().calculate(filtered_data, group_by)



