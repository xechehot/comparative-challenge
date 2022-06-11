import pandas as pd

from lib.combiner import MetricCombiner
from lib.metric import TotalPurchasedAmountMetric, AvgPurchasedAmountPerPayingUserMetric, Metric
from lib.metric_pair import MetricPair
from lib.significant_condition import AndSignificantCondition, ChangeAbsolutePercentageSignificantCondition, \
    ChangeAbsoluteValueSignificantCondition

CHANGE_ABSOLUTE_PERCENTAGE_THRESHOLD = 0.02
CHANGE_ABSOLUTE_VALUE_THRESHOLD = 0.02

YESTERDAY_FIELD = 'purchased_amount_yesterday'
TODAY_FIELD = 'purchased_amount_today'
DIMENSIONS = ['country', 'is_vip']

if __name__ == '__main__':
    absolute_percentage_condition = ChangeAbsolutePercentageSignificantCondition(CHANGE_ABSOLUTE_PERCENTAGE_THRESHOLD)
    absolute_value_condition = ChangeAbsoluteValueSignificantCondition(CHANGE_ABSOLUTE_VALUE_THRESHOLD)
    significant_condition = AndSignificantCondition([absolute_value_condition, absolute_percentage_condition])

    total_purchase_amount = MetricPair(TotalPurchasedAmountMetric(YESTERDAY_FIELD),
                                       TotalPurchasedAmountMetric(TODAY_FIELD))
    avg_purchased_amount_per_paying_user = MetricPair(AvgPurchasedAmountPerPayingUserMetric(YESTERDAY_FIELD),
                                                      AvgPurchasedAmountPerPayingUserMetric(TODAY_FIELD))
    metrics = [total_purchase_amount, avg_purchased_amount_per_paying_user]
    combiner = MetricCombiner(metrics, significant_condition)

    data = pd.read_csv('data/users_data.csv')
    metric_results = combiner.combine(data, DIMENSIONS)
    for metric in metric_results:
        print(metric)
