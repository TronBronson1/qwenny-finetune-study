import copy
import pytest
from subject import interval_union

class TestIntervalUnionValues:
    def assert_exact_equal(self, actual, expected):
        assert type(actual) is type(expected)
        assert actual == expected

    def test_single_interval(self):
        args, expected = ([(1, 5)]), [(1, 5)]
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_touching_intervals(self):
        args, expected = ([(1, 2), (2, 3)]), [(1, 3)]
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_overlapping_intervals(self):
        args, expected = ([(1, 5), (3, 7)]), [(1, 7)]
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_disjoint_intervals(self):
        args, expected = ([(1, 3), (5, 7)]), [(1, 3), (5, 7)]
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_complex_merge(self):
        args, expected = ([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)]
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_empty_input(self):
        args, expected = ([], [])
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_three_way_merge(self):
        args, expected = ([(1, 5), (4, 8), (6, 10)]), [(1, 10)]
        actual = interval_union(*args)
        self.assert_exact_equal(actual, expected)

    def test_input_is_unmodified(self):
        orig = copy.deepcopy([(1, 5), (3, 7), (2, 4)])
        actual = interval_union(*orig)
        assert orig == [(1, 5), (3, 7), (2, 4)]

class TestIntervalUnionTypes:
    def assert_returned_types(self, actual):
        assert type(actual) is list
        for elem in actual:
            assert type(elem) is tuple
            assert len(elem) == 2
            assert type(elem[0]) is int
            assert type(elem[1]) is int

class TestIntervalUnionInvalidTypes:
    def test_list_of_ints_raises(self):
        with pytest.raises(TypeError):
            interval_union([1, 2], [3, 4])

    def test_list_of_tup_strings_raises(self):
        with pytest.raises(TypeError):
            interval_union(("a", "b"))

    def test_list_of_floats_raises(self):
        with pytest.raises(TypeError):
            interval_union([1.0, 2.0])

    def test_list_of_none_raises(self):
        with pytest.raises(TypeError):
            interval_union([None])

    def test_list_of_bad_nested_types_raises(self):
        with pytest.raises(TypeError):
            interval_union([(1, 5.0), (3, 7)])

    def test_scalar_int_raises(self):
        with pytest.raises(TypeError):
            interval_union(5)

    def test_scalar_list_raises(self):
        with pytest.raises(TypeError):
            interval_union([1, 2])

class TestIntervalUnionInvalidValue:
    def test_low_ge_high_raises(self):
        with pytest.raises(ValueError):
            interval_union([(1, 1)])

    def test_low_gte_high_raises(self):
        with pytest.raises(ValueError):
            interval_union([(1, 0)])

    def test_tuple_not_exact_raises(self):
        with pytest.raises(TypeError):
            interval_union([1, 2], [3, 4])

    def test_list_element_not_tuple_raises(self):
        with pytest.raises(TypeError):
            interval_union([1, 2, 3], [4, 5])
