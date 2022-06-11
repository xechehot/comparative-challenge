import pytest

from lib.segment_name_provider import CountrySegmentNameProvider, IsVipSegmentNameProvider, UsersSegmentNameProvider
from lib.segment_name_provider_factory import UsersSegmentNameProviderFactory


# noinspection PyTypeChecker
def test_user_segment_name_provider_factory():
    provider_map = {
        'country': CountrySegmentNameProvider,
        'is_vip': IsVipSegmentNameProvider
    }
    factory = UsersSegmentNameProviderFactory(provider_map)
    country_provider = factory.get_segment_name_provider(['country'])
    assert type(country_provider) == UsersSegmentNameProvider
    assert len(country_provider.providers) == 1
    assert country_provider.providers[0] is CountrySegmentNameProvider

    country_vip_provider = factory.get_segment_name_provider(['country', 'is_vip'])
    assert type(country_vip_provider) == UsersSegmentNameProvider
    assert len(country_vip_provider.providers) == 2
    assert country_vip_provider.providers[0] is CountrySegmentNameProvider
    assert country_vip_provider.providers[1] is IsVipSegmentNameProvider


def test_no_provider_for_dimension():
    factory = UsersSegmentNameProviderFactory({})
    with pytest.raises(NotImplementedError, match='There is no provider for dimension age'):
        factory.get_segment_name_provider(['age'])
