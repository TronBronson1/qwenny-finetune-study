```python
from subject import row_major_offset
import pytest


class TestRowMajorOffset:
    def test_valid_offset_0_0(self):
        row = 0
        column = 0
        rows = 2
        columns = 3
        expected = 0
        assert row_major_offset(row, column, rows, columns) == expected

    def test_valid_offset_1_2(self):
        row = 1
        column = 2
        rows = 2
        columns = 3
        expected = 5
        assert row_major_offset(row, column, rows, columns) == expected

    def test_valid_offset_max(self):
        row = 1
        column = 2
        rows = 2
        columns = 3
        expected = 5
        assert row_major_offset(row, column, rows, columns) == expected

    def test_invalid_type_row_bool(self):
        with pytest.raises(TypeError):
            row_major_offset(True, 0, 2, 3)

    def test_invalid_type_column_bool(self):
        with pytest.raises(TypeError):
            row_major_offset(0, True, 2, 3)

    def test_invalid_type_rows_bool(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, True, 3)

    def test_invalid_type_columns_bool(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, 2, True)

    def test_invalid_type_row_float(self):
        with pytest.raises(TypeError):
            row_major_offset(0.0, 0, 2, 3)

    def test_invalid_type_column_float(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0.0, 2, 3)

    def test_invalid_type_rows_float(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, 0.0, 3)

    def test_invalid_type_columns_float(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, 2, 0.0)

    def test_invalid_type_row_string(self):
        with pytest.raises(TypeError):
            row_major_offset("0", 0, 2, 3)

    def test_invalid_type_column_string(self):
        with pytest.raises(TypeError):
            row_major_offset(0, "0", 2, 3)

    def test_invalid_type_rows_string(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, "2", 3)

    def test_invalid_type_columns_string(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, 2, "3")

    def test_invalid_value_rows_zero(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, 0, 3)

    def test_invalid_value_rows_negative(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, -1, 3)

    def test_invalid_value_columns_zero(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, 2, 0)

    def test_invalid_value_columns_negative(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, 2, -1)

    def test_invalid_index_row_too_large(self):
        with pytest.raises(IndexError):
            row_major_offset(2, 0, 2, 3)

    def test_invalid_index_row_negative(self):
        with pytest.raises(IndexError):
            row_major_offset(-1, 0, 2, 3)

    def test_invalid_index_column_too_large(self):
        with pytest.raises(IndexError):
            row_major_offset(0, 3, 2, 3)

    def test_invalid_index_column_negative(self):
        with pytest.raises(IndexError):
            row_major_offset(0, -1, 2, 3)

    def test_reversed_bounds_row_exceeds_rows(self):
        with pytest.raises(IndexError):
            row_major_offset(2, 0, 2, 3)

    def test_reversed_bounds_column_exceeds_columns(self):
        with pytest.raises(IndexError):
            row_major_offset(0, 3, 2, 3)

    def test_reversed_bounds_multiple_invalid(self):
        with pytest.raises(IndexError):
            row_major_offset(2, 3, 2, 3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Requirement-to-Input Mapping
- `row`: built-in `int` only; `bool`, `float`, `str`, or negative values rejected via `TypeError` or `IndexError`.
- `column`: built-in `int` only; `bool`, `float`, `str`, or negative values rejected via `TypeError` or `IndexError`.
- `rows`: built-in `int` only; must be `> 0`; otherwise `TypeError` (if non-int) or `ValueError` (if <= 0).
- `columns`: built-in `int` only; must be `> 0`; otherwise `TypeError` (if non-int) or `ValueError` (if <= 0).
- Index bounds: `0 <= row < rows` and `0 <= column < columns`; violations raise `IndexError`.
- Return: exact built-in `int` representing `row * columns + column`.

### Honest Finite-Coverage Limitations
This test suite explicitly validates a representative subset of edge cases (zero indices, maximum valid indices, exact type boundaries like booleans and floats, and reversed-bound scenarios). It does not claim to cover:
- All possible integer combinations within valid bounds (infinite cases).
- Subclasses of `int` (e.g., custom int subclasses) beyond the provided examples, as Python’s duck typing allows them to pass type checks unless explicitly restricted.
- Any future or undocumented behavior of `row_major_offset` not described in the contract.
- Performance or memory constraints, as the function contract does not specify them.