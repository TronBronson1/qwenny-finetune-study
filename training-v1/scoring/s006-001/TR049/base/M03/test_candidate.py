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
