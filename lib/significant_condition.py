from abc import ABC, abstractmethod
from functools import reduce
from typing import List

from lib.metric_pair import MetricPair


class SignificantCondition(ABC):
    @abstractmethod
    def is_satisfied(self, overall: MetricPair, segment: MetricPair):
        pass


class AndSignificantCondition(SignificantCondition):
    def __init__(self, conditions: List[SignificantCondition]):
        self.conditions = conditions

    def is_satisfied(self, overall: MetricPair, segment: MetricPair):
        conditions_result = map(lambda condition: condition.is_satisfied(overall, segment), self.conditions)
        return reduce(lambda x, y: x & y, conditions_result)


class ChangeAbsolutePercentageSignificantCondition(SignificantCondition):
    def __init__(self, percentage):
        self.percentage = percentage

    def is_satisfied(self, overall: MetricPair, segment: MetricPair):
        diff = abs(segment.change_percentage) - abs(overall.change_percentage)
        # TODO Does we need to take abs from diff here?
        return diff > self.percentage


class ChangeAbsoluteValueSignificantCondition(SignificantCondition):
    def __init__(self, percentage):
        self.percentage = percentage

    def is_satisfied(self, overall: MetricPair, segment: MetricPair):
        overall_percentage = abs(overall.change_value) * self.percentage
        return abs(segment.change_value) > overall_percentage
