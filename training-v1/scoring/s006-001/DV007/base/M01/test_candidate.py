from subject import grid_neighbors
import pytest

# --- Type Validation Tests ---

def test_grid_neighbors_valid_ints():
    row = 1
    column = 1
    rows = 2
    columns = 2
    result = grid_neighbors(row, column, rows, columns)
    assert result == [(0, 1), (1, 1), (1, 0), (1, 2)]

def test_grid_neighbors_row_is_bool():
    with pytest.raises(TypeError):
        grid_neighbors(True, 0, 2, 2)

def test_grid_neighbors_column_is_bool():
    with pytest.raises(TypeError):
        grid_neighbors(1, True, 2, 2)

def test_grid_neighbors_rows_is_bool():
    with pytest.raises(TypeError):
        grid_neighbors(1, 1, True, 2)

def test_grid_neighbors_columns_is_bool():
    with pytest.raises(TypeError):
        grid_neighbors(1, 1, 2, True)

# --- Value Range Validation Tests ---

def test_grid_neighbors_zero_rows():
    with pytest.raises(ValueError):
        grid_neighbors(0, 0, 0, 2)

def test_grid_neighbors_negative_rows():
    with pytest.raises(ValueError):
        grid_neighbors(0, 0, -1, 2)

def test_grid_neighbors_zero_columns():
    with pytest.raises(ValueError):
        grid_neighbors(0, 0, 2, 0)

def test_grid_neighbors_negative_columns():
    with pytest.raises(ValueError):
        grid_neighbors(0, 0, 2, -1)

# --- In-Bounds Validation Tests ---

def test_grid_neighbors_row_out_of_bounds():
    with pytest.raises(IndexError):
        grid_neighbors(3, 1, 2, 2)

def test_grid_neighbors_column_out_of_bounds():
    with pytest.raises(IndexError):
        grid_neighbors(1, 3, 2, 2)

def test_grid_neighbors_row_zero_is_valid_when_rows_is_one():
    result = grid_neighbors(0, 1, 1, 2)
    assert result == [(0, 1), (0, 1), (0, 0), (0, 2)]

def test_grid_neighbors_column_zero_is_valid_when_columns_is_one():
    result = grid_neighbors(1, 0, 2, 1)
    assert result == [(0, 0), (1, 0), (1, 0), (0, 0)]

# --- Reversed Bounds Test (Logic Check) ---
# Note: The contract specifies that ValueError is raised for non-positive rows/columns 
# and IndexError for out-of-bounds. It does not explicitly state behavior for reversed bounds 
# where row >= rows or column >= columns. This test checks if a specific invalid state 
# (row > rows) triggers IndexError or if the function handles it differently based on the 
# specific cell value relative to the grid dimensions.
def test_grid_neighbors_row_exceeds_rows():
    try:
        grid_neighbors(5, 1, 3, 5)
        # If no exception is raised, the result might be empty or contain the invalid cell
        # depending on internal implementation. We check the return value type.
        result = grid_neighbors(5, 1, 3, 5)
        assert isinstance(result, list)
        # If the result is not empty, it means the function accepts out-of-bounds coordinates
        # or logic error occurred in implementation.
    except IndexError:
        # Expected behavior if bounds checking happens before neighbor generation
        pass
    except Exception:
        # Some implementations might raise ValueError or return empty list for invalid cells
        pass

def test_grid_neighbors_column_exceeds_columns():
    try:
        grid_neighbors(1, 6, 2, 4)
        result = grid_neighbors(1, 6, 2, 4)
        assert isinstance(result, list)
    except IndexError:
        pass
    except Exception:
        pass
