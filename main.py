import pandas as pd

from lib.combiner import MetricCombiner
from lib.metric import TotalPurchasedAmountMetric, AvgPurchasedAmountPerPayingUserMetric, Metric
from lib.metric_pair import MetricPair
from lib.segment_name_provider import CountrySegmentNameProvider, IsVipSegmentNameProvider
from lib.segment_name_provider_factory import UsersSegmentNameProviderFactory
from lib.significant_condition import AndSignificantCondition, ChangeAbsolutePercentageSignificantCondition, \
    ChangeAbsoluteValueSignificantCondition

CHANGE_ABSOLUTE_PERCENTAGE_THRESHOLD = 0.02
CHANGE_ABSOLUTE_VALUE_THRESHOLD = 0.02

YESTERDAY_FIELD = 'purchased_amount_yesterday'
TODAY_FIELD = 'purchased_amount_today'
DIMENSIONS = ['country', 'is_vip']


def get_segment_name_provider_factory():
    segment_name_provider_map = {
        'country': CountrySegmentNameProvider(),
        'is_vip': IsVipSegmentNameProvider()
    }
    return UsersSegmentNameProviderFactory(segment_name_provider_map)


def get_metrics():
    total_purchase_amount = MetricPair(TotalPurchasedAmountMetric(YESTERDAY_FIELD),
                                       TotalPurchasedAmountMetric(TODAY_FIELD))
    avg_purchased_amount_per_paying_user = MetricPair(AvgPurchasedAmountPerPayingUserMetric(YESTERDAY_FIELD),
                                                      AvgPurchasedAmountPerPayingUserMetric(TODAY_FIELD))
    return [total_purchase_amount, avg_purchased_amount_per_paying_user]


def get_significant_condition():
    absolute_percentage_condition = ChangeAbsolutePercentageSignificantCondition(CHANGE_ABSOLUTE_PERCENTAGE_THRESHOLD)
    absolute_value_condition = ChangeAbsoluteValueSignificantCondition(CHANGE_ABSOLUTE_VALUE_THRESHOLD)
    return AndSignificantCondition([absolute_percentage_condition, absolute_value_condition])


if __name__ == '__main__':
    significant_condition = get_significant_condition()
    metrics = get_metrics()
    users_segment_name_provider_factory = get_segment_name_provider_factory()
    combiner = MetricCombiner(metrics, significant_condition, users_segment_name_provider_factory)

    data = pd.read_csv('data/users_data.csv')
    metric_results = combiner.combine(data, DIMENSIONS)
    for metric in metric_results:
        print(metric)
