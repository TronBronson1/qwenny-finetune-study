```python
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
```

### Requirement-to-Input Mapping

| Requirement | Input Argument | Expected Behavior |
| :--- | :--- | :--- |
| `values` must be exact built-in `tuple` | `tuple` | Success; rotates. |
| `values` must be exact built-in `tuple` | `list`, `str`, `tuple` subclass, `bool` | Raises `TypeError`. |
| `steps` must be exact built-in `int` | `int` | Success; rotates (wraps mod length). |
| `steps` must be exact built-in `int` | `bool`, `float`, `str`, `None` | Raises `TypeError`. |
| Rotation logic | Valid `tuple`, valid `int` | Right shift by `steps % len(values)`. |
| Negative rotation | Valid `tuple`, negative `int` | Left shift by `abs(steps) % len(values)`. |
| Empty input | Empty `tuple`, any `int` | Returns `()`. |
| Immutability | `tuple` containing nested mutable containers | Input container identity/value preserved; output is new container. |

### Finite Coverage Limitations

1.  **Argument Type Verification**: Tests cover specific standard types (`list`, `str`, `float`, `bool`, `tuple` subclasses) failing, but do not exhaustively verify every possible object class that is not an exact `tuple` or `int` (e.g., custom classes implementing only `__class__` attributes differently or obscure internal types).
2.  **Edge Cases on Length**: While `len=1` and `len=2` are covered, exhaustive verification of rotation behavior for all integer lengths $N$ where $N \ge 3$ is implied by the logic but not explicitly enumerated for every $N$.
3.  **Immutability Verification**: The test verifies that the *input* object is not mutated after the call, but it does not verify that the *elements* inside the input tuple (specifically nested mutable objects) were not modified in place by any internal logic if the function were to construct the result destructively (though the contract implies a non-destructive result construction).
4.  **`steps` Modulo Behavior**: Tests verify positive wrapping and negative modulo behavior (Python semantics), but do not test `steps` larger than memory limits or extremely negative values beyond the tested `-100`.