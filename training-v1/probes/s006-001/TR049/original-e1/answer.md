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
        assert row_major_offset(row, column, rows, columns) is expected

    def test_valid_offset_1_2(self):
        row = 1
        column = 2
        rows = 2
        columns = 3
        expected = 5
        assert row_major_offset(row, column, rows, columns) is expected

    def test_valid_offset_max(self):
        row = 1
        column = 2
        rows = 2
        columns = 3
        expected = 5
        assert row_major_offset(row, column, rows, columns) is expected

    def test_invalid_type_row(self):
        with pytest.raises(TypeError):
            row_major_offset(True, 0, 2, 3)

    def test_invalid_type_column(self):
        with pytest.raises(TypeError):
            row_major_offset(0, True, 2, 3)

    def test_invalid_type_rows(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, True, 3)

    def test_invalid_type_columns(self):
        with pytest.raises(TypeError):
            row_major_offset(0, 0, 2, True)

    def test_value_error_rows_zero(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, 0, 3)

    def test_value_error_rows_negative(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, -1, 3)

    def test_value_error_columns_zero(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, 2, 0)

    def test_value_error_columns_negative(self):
        with pytest.raises(ValueError):
            row_major_offset(0, 0, 2, -1)

    def test_index_error_row_too_large(self):
        with pytest.raises(IndexError):
            row_major_offset(3, 0, 2, 3)

    def test_index_error_column_too_large(self):
        with pytest.raises(IndexError):
            row_major_offset(0, 3, 2, 3)

    def test_index_error_row_negative(self):
        with pytest.raises(IndexError):
            row_major_offset(-1, 0, 2, 3)

    def test_index_error_column_negative(self):
        with pytest.raises(IndexError):
            row_major_offset(0, -1, 2, 3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Requirement-to-Input Mapping
- **Input types**: All four parameters must be `int`; `bool` is rejected via `TypeError`.
- **Shape validation**: `rows > 0` and `columns > 0`; otherwise `ValueError`.
- **Bounds validation**: `0 <= row < rows` and `0 <= column < columns`; otherwise `IndexError`.
- **Return**: `row * columns + column` as a built-in `int`.

### Finite-Coverage Limitations
- Only a handful of valid offsets were tested (0,0), (1,2), and (max). Not all `(r, c)` pairs up to large dimensions are exercised.
- Only a few boundary cases for `TypeError` (`True` as int) and `ValueError` (zero/negative dimensions) were checked.
- No negative dimension combinations beyond single-zero cases were verified.
- No stress tests for very large integers or dimensions.
- No tests for subclasses of `int` (e.g., custom integer-like objects) beyond explicit `bool` rejection.