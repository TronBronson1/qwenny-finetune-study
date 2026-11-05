from subject import interval_union
import pytest

@pytest.mark.parametrize("intervals,expected", [
    # Single interval
    ([(-1, 1)], [(-1, 1)]),
    # Multiple disjoint intervals
    ([(0, 2), (5, 8)], [(0, 2), (5, 8)]),
    # Overlapping intervals (merge)
    ([(0, 5), (2, 6)], [(0, 6)]),
    # Touching intervals (merge)
    ([(0, 2), (2, 5)], [(0, 5)]),
    # Unsorted input intervals
    ([(3, 5), (0, 2), (1, 2)], [(0, 2), (1, 2), (3, 5)]),
    # Single point interval (should be merged or kept depending on logic, here kept as disjoint set if not touching others)
    # Note: Contract says low < high. A single point (1, 1) would be ValueError.
    # Testing merging of multiple disjoint points is impossible per contract (low<high).
    # Testing merging of intervals that result in a gap filled is impossible per contract definition of half-open union usually.
    # Standard half-open union logic: [0, 2) U [1, 3) -> [0, 3).
    ([(0, 2), (1, 3)], [(0, 3)]),
    # Nested intervals
    ([(0, 10), (2, 5)], [(0, 10)]),
    # Complex merging
    ([(0, 3), (2, 5), (6, 8)], [(0, 5), (6, 8)]),
    # Empty list
    ([], []),
])
def test_interval_union_valid(intervals, expected):
    result = interval_union(intervals)
    assert result == expected

@pytest.mark.parametrize("intervals", [
    # Invalid types
    ("not a list", None),
    ([1, 2], None),
    ([(1,)], None),
    ([(1, 2, 3)], None),
    ([(1, "2")], None),
    # Invalid value logic (low >= high)
    ([(1, 1)], None),
    ([(1, 0)], None),
    # Non-iterable elements (simulated by passing a list containing non-tuple)
    ([1], None), # List of ints instead of tuples
])
def test_interval_union_invalid(intervals):
    with pytest.raises((TypeError, ValueError)):
        interval_union(intervals)

