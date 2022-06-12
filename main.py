import argparse
import time
from typing import List

import pandas as pd

from lib.combiner import MetricCombiner
from lib.metric import TotalPurchasedAmountMetric, AvgPurchasedAmountPerPayingUserMetric
from lib.metric_pair import MetricPair
from lib.segment_name_provider import CountrySegmentNameProvider, IsVipSegmentNameProvider
from lib.segment_name_provider_factory import UsersSegmentNameProviderFactory, SegmentNameProviderFactory
from lib.significant_condition import AndSignificantCondition, ChangeAbsolutePercentageSignificantCondition, \
    ChangeAbsoluteValueSignificantCondition, SignificantCondition

N_CORES = 2
CHANGE_ABSOLUTE_PERCENTAGE_THRESHOLD = 0.02
CHANGE_ABSOLUTE_VALUE_THRESHOLD = 0.02

YESTERDAY_FIELD = 'purchased_amount_yesterday'
TODAY_FIELD = 'purchased_amount_today'
DIMENSIONS = ['country', 'is_vip']


def get_segment_name_provider_factory() -> SegmentNameProviderFactory:
    segment_name_provider_map = {
        'country': CountrySegmentNameProvider(),
        'is_vip': IsVipSegmentNameProvider()
    }
    return UsersSegmentNameProviderFactory(segment_name_provider_map)


def get_metrics() -> List[MetricPair]:
    total_purchase_amount = MetricPair(TotalPurchasedAmountMetric(YESTERDAY_FIELD),
                                       TotalPurchasedAmountMetric(TODAY_FIELD))
    avg_purchased_amount_per_paying_user = MetricPair(AvgPurchasedAmountPerPayingUserMetric(YESTERDAY_FIELD),
                                                      AvgPurchasedAmountPerPayingUserMetric(TODAY_FIELD))
    return [total_purchase_amount, avg_purchased_amount_per_paying_user]


def get_significant_condition() -> SignificantCondition:
    absolute_percentage_condition = ChangeAbsolutePercentageSignificantCondition(CHANGE_ABSOLUTE_PERCENTAGE_THRESHOLD)
    absolute_value_condition = ChangeAbsoluteValueSignificantCondition(CHANGE_ABSOLUTE_VALUE_THRESHOLD)
    return AndSignificantCondition([absolute_percentage_condition, absolute_value_condition])


def main(path):
    significant_condition = get_significant_condition()
    metrics = get_metrics()
    users_segment_name_provider_factory = get_segment_name_provider_factory()
    combiner = MetricCombiner(metrics, significant_condition, users_segment_name_provider_factory, N_CORES)
    raw_data = pd.read_csv(path)
    for size in [1, 10, 100, 1000, 2000]:
        data = pd.concat(raw_data.sample(frac=1) for _ in range(size))
        print('Size is %s' % len(data))
        start_time = time.time()
        metric_results = combiner.combine(data, DIMENSIONS)
        print(" combine: %s seconds" % (time.time() - start_time))
        start_time = time.time()
        metric_results = combiner.parallel_combine(data, DIMENSIONS)
        print(" parallel_combine: %s seconds" % (time.time() - start_time))
    # for metric in metric_results:
    #     print(metric)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print our all significant segments by given users data')
    parser.add_argument('--path',
                        help='Path to a csv-file with users data',
                        default='data/users_data.csv')
    args = parser.parse_args()

    main(args.path)
