from itertools import starmap, combinations, repeat


def subslices(iterable):
    """Return all contiguous non-empty subslices of *iterable* with indexe of subset.
    """
    seq = list(iterable)
    slices = starmap(slice, combinations(range(len(seq) + 1), 2))

    return map(lambda v, s: (s.start, v[s]), repeat(seq), slices)
