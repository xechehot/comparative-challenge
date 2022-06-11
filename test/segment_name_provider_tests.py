from lib.segment_name_provider import IsVipSegmentNameProvider, CountrySegmentNameProvider, UsersSegmentNameProvider


def test_is_vip_segment_provider():
    provider = IsVipSegmentNameProvider()
    assert provider.get_segment_name(False) == 'who are not VIP'
    assert provider.get_segment_name(True) == 'who are VIP'


def test_country_segment_provider():
    provider = CountrySegmentNameProvider()
    assert provider.get_segment_name('canada') == 'from Canada'
    assert provider.get_segment_name('CANADA') == 'from Canada'


def test_users_country_segment_provider():
    country_provider = CountrySegmentNameProvider()
    users_provider = UsersSegmentNameProvider([country_provider])
    assert users_provider.get_segment_name('canada') == 'Users from Canada'
    assert users_provider.get_segment_name(('canada',)) == 'Users from Canada'


def test_users_is_vip_segment_provider():
    is_vip_provider = IsVipSegmentNameProvider()
    users_provider = UsersSegmentNameProvider([is_vip_provider])
    assert users_provider.get_segment_name(False) == 'Users who are not VIP'
    assert users_provider.get_segment_name([False]) == 'Users who are not VIP'


def test_users_country_and_is_vip_segment_provider():
    country_provider = CountrySegmentNameProvider()
    is_vip_provider = IsVipSegmentNameProvider()
    users_provider = UsersSegmentNameProvider([country_provider, is_vip_provider])
    assert users_provider.get_segment_name(('canada', False)) == 'Users from Canada and who are not VIP'
    assert users_provider.get_segment_name(['brazil', True]) == 'Users from Brazil and who are VIP'
