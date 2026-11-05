from subject import rotate_right
import pytest

# --- Type Validation Tests ---

def test_rotate_right_valid_tuple_int():
    args = ( (1, 2, 3), 1 )
    assert rotate_right(*args) == (3, 1, 2)

def test_rotate_right_valid_tuple_zero():
    args = ( (1, 2, 3), 0 )
    assert rotate_right(*args) == (1, 2, 3)

def test_rotate_right_valid_tuple_negative():
    args = ( (1, 2, 3), -1 )
    assert rotate_right(*args) == (2, 3, 1)

def test_rotate_right_valid_tuple_large_steps():
    args = ( (1, 2, 3), 100 )
    assert rotate_right(*args) == (1, 2, 3) # 100 % 3 == 1

def test_rotate_right_empty_tuple():
    args = ( (), 1 )
    assert rotate_right(*args) == ()

def test_rotate_right_empty_tuple_large_steps():
    args = ( (), 100 )
    assert rotate_right(*args) == ()

def test_rotate_right_tuple_subclass_invalid_type():
    with pytest.raises(TypeError):
        rotate_right( (1, 2, 3), 1 )

def test_rotate_right_list_invalid_type():
    with pytest.raises(TypeError):
        rotate_right( [1, 2, 3], 1 )

def test_rotate_right_string_invalid_type():
    with pytest.raises(TypeError):
        rotate_right( "abc", 1 )

def test_rotate_right_bool_invalid_type():
    with pytest.raises(TypeError):
        rotate_right( (1, 2, 3), True )

def test_rotate_right_float_invalid_type():
    with pytest.raises(TypeError):
        rotate_right( (1, 2, 3), 1.0 )

# --- Value & Shape Validation Tests ---

def test_rotate_right_single_element():
    args = ( ("a",), 1 )
    assert rotate_right(*args) == ("a",)

def test_rotate_right_two_elements_right():
    args = ( ("x", "y"), 1 )
    assert rotate_right(*args) == ("y", "x")

def test_rotate_right_two_elements_left():
    args = ( ("x", "y"), -1 )
    assert rotate_right(*args) == ("y", "x")

def test_rotate_right_nested_containers_immutable():
    # Ensure input tuple is not mutated, even if result is constructed differently
    nested_input = ( [1, 2], [3, 4] )
    result = rotate_right( nested_input, 1 )
    
    # Verify result structure
    assert result == ( [3, 4], [1, 2] )
    
    # Verify input tuple contents are unchanged (identity check on tuple content)
    assert nested_input == ( [1, 2], [3, 4] )
    assert nested_input is not result

def test_rotate_right_large_steps_wraps_correctly():
    args = ( ("a", "b", "c", "d"), 5 )
    assert rotate_right(*args) == ("c", "d", "a", "b") # 5 % 4 == 1

def test_rotate_right_large_steps_wraps_left():
    args = ( ("a", "b", "c", "d"), -1 )
    assert rotate_right(*args) == ("d", "a", "b", "c")

def test_rotate_right_negative_steps_large_magnitude():
    args = ( ("a", "b", "c", "d"), -100 )
    # -100 % 4 is 0 in Python, so result should be identity
    assert rotate_right(*args) == ("a", "b", "c", "d")
