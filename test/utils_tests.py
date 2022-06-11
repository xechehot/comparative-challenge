from lib.utils import subslices


def test_subslices_of_two():
    expected = [(0, ['country']), (0, ['country', 'is_vip']), (1, ['is_vip'])]
    actual = subslices(['country', 'is_vip'])
    assert type(actual) == map
    assert list(actual) == expected


def test_subslices_of_three():
    expected = [(0, ['A']),
                (0, ['A', 'B']),
                (0, ['A', 'B', 'C']),
                (1, ['B']),
                (1, ['B', 'C']),
                (2, ['C'])]
    actual = subslices('ABC')
    assert type(actual) == map
    assert list(actual) == expected
