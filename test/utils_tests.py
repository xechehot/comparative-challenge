from lib.utils import subslices


def test_subslices_of_two():
    expected = [['country'], ['country', 'is_vip'], ['is_vip']]
    actual = subslices(['country', 'is_vip'])
    assert type(actual) == map
    assert list(actual) == expected


def test_subslices_of_three():
    expected = [['A'], ['A', 'B'], ['A', 'B', 'C'], ['B'], ['B', 'C'], ['C']]
    actual = subslices('ABC')
    assert type(actual) == map
    assert list(actual) == expected
