```python
from subject import run_length_encode
import pytest


class TestTypeErrorRejection:
    def test_non_list_input(self):
        with pytest.raises(TypeError):
            run_length_encode("not a list")

    def test_list_with_non_string_elements(self):
        with pytest.raises(TypeError):
            run_length_encode(["a", 1, "b"])

    def test_nested_non_string_in_list(self):
        with pytest.raises(TypeError):
            run_length_encode(["a", ["b"]])

    def test_list_with_none(self):
        with pytest.raises(TypeError):
            run_length_encode(["a", None, "b"])

    def test_list_with_tuple_element(self):
        with pytest.raises(TypeError):
            run_length_encode(["a", ("b", "c")])


class TestEmptyInput:
    def test_empty_list(self):
        assert run_length_encode([]) == []


class TestSingleElement:
    def test_single_element(self):
        assert run_length_encode(["a"]) == [("a", 1)]


class TestConsecutiveRuns:
    def test_two_identical(self):
        assert run_length_encode(["a", "a"]) == [("a", 2)]

    def test_three_identical(self):
        assert run_length_encode(["a", "a", "a"]) == [("a", 3)]

    def test_four_identical(self):
        assert run_length_encode(["a", "a", "a", "a"]) == [("a", 4)]

    def test_five_identical(self):
        assert run_length_encode(["a", "a", "a", "a", "a"]) == [("a", 5)]


class TestSeparatedRuns:
    def test_single_run_then_different(self):
        assert run_length_encode(["a", "b"]) == [("a", 1), ("b", 1)]

    def test_two_runs_separated(self):
        assert run_length_encode(["a", "b", "c"]) == [("a", 1), ("b", 1), ("c", 1)]

    def test_two_runs_separated_identical_strings(self):
        assert run_length_encode(["a", "b", "a"]) == [("a", 1), ("b", 1), ("a", 1)]


class TestMixedTypesError:
    def test_int_in_list(self):
        with pytest.raises(TypeError):
            run_length_encode([1, 2, 3])

    def test_float_in_list(self):
        with pytest.raises(TypeError):
            run_length_encode([1.0, 2.0, 3.0])

    def test_dict_in_list(self):
        with pytest.raises(TypeError):
            run_length_encode([{"a": 1}])


class TestReturnTypeValidation:
    def test_return_type_is_list(self):
        result = run_length_encode(["a", "b"])
        assert isinstance(result, list)

    def test_return_elements_are_tuples(self):
        result = run_length_encode(["a", "a", "b"])
        for elem in result:
            assert isinstance(elem, tuple)

    def test_return_tuple_has_string_and_int(self):
        result = run_length_encode(["a", "a", "a"])
        for elem in result:
            assert len(elem) == 2
            assert isinstance(elem[0], str)
            assert isinstance(elem[1], int)


class TestImmutableInput:
    def test_input_not_mutated(self):
        original = ["a", "b", "a"]
        copy = original.copy()
        run_length_encode(original)
        assert original == copy
```

**Requirement-to-Input Mapping:**
- `TypeError` raised for non-list inputs.
- `TypeError` raised for lists containing non-string elements (including nested structures).
- Empty list returns empty list.
- Consecutive identical strings grouped into single tuple with incremented count.
- Non-consecutive identical strings remain as separate tuples.
- Input lists remain unmutated after call.
- Returned values are built-in types (`list`, `tuple`, `str`, `int`), not subclasses.

**Finite-Coverage Limitations:**
This test suite does not cover:
- Subclasses of `str` or `list` as inputs.
- Custom string-like objects that pass `isinstance(x, str)` checks via duck typing.
- Deeply nested invalid structures beyond one level of inspection.
- Extremely large inputs (e.g., > 10⁶ elements) for performance or memory constraints.
- Unicode-specific edge cases beyond basic string equality.