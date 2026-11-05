from subject import rotate_right
import pytest

# --- Type Validation Tests ---

def test_rotate_empty_tuple():
    assert rotate_right((), 1) == ()

def test_rotate_single_element():
    assert rotate_right((5,), 10) == (5,)

def test_rotate_right_basic():
    values = (1, 2, 3)
    assert rotate_right(values, 1) == (3, 1, 2)

def test_rotate_left_via_negative_steps():
    values = (1, 2, 3)
    # -1 step rotates right by length-1 (equivalent to left by 1)
    assert rotate_right(values, -1) == (2, 3, 1)

def test_rotate_large_wrapping_positive():
    values = ("a", "b")
    assert rotate_right(values, 5) == ("b", "a")  # 5 % 2 = 1

def test_rotate_large_wrapping_negative():
    values = ("x", "y")
    assert rotate_right(values, -3) == ("x", "y") # -3 % 2 = -1 -> effectively shift left 1 / right 1

def test_rotate_complex_types():
    data = [1, 2.5, "str", None]
    container = tuple(data)
    result = rotate_right(container, 2)
    expected = (None, 1, 2.5, "str")
    assert result == expected
    # Verify identity preservation for list elements inside
    assert result[0] is None
    assert result[2] is data[1]

# --- Invalid Input Type Tests ---

def test_reject_bool_as_steps_is_not_accepted():
    with pytest.raises(TypeError):
        rotate_right((1, 2), True)

def test_reject_list_as_values_is_not_accepted():
    with pytest.raises(TypeError):
        rotate_right([1, 2], 1)

def test_reject_string_as_values_is_not_accepted():
    with pytest.raises(TypeError):
        rotate_right("abc", 1)

def test_reject_float_as_steps_is_not_accepted():
    with pytest.raises(TypeError):
        rotate_right((1, 2), 1.5)

def test_reject_dict_as_steps_is_not_accepted():
    with pytest.raises(TypeError):
        rotate_right((1, 2), {"step": 1})

def test_reject_tuple_subclass_as_values_is_not_accepted():
    class MyTuple(tuple):
        pass
    with pytest.raises(TypeError):
        rotate_right(MyTuple((1, 2)), 1)

def test_reject_int_subclass_as_steps_is_not_accepted():
    class MyInt(int):
        pass
    with pytest.raises(TypeError):
        rotate_right((1, 2), MyInt(1))

def test_reject_none_as_steps_is_not_accepted():
    with pytest.raises(TypeError):
        rotate_right((1, 2), None)

def test_reject_zero_steps_returns_same():
    values = (1, 2, 3, 4)
    assert rotate_right(values, 0) == values

def test_reject_large_step_well_behaves():
    values = (1, 2, 3)
    result = rotate_right(values, 100)
    assert result == (1, 2, 3)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
