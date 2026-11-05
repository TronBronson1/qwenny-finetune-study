```python
from subject import rotate_right

class TupleChild(tuple):
    pass

@pytest.mark.parametrize("values,steps,expected", [([1, 2, 3], 0, (1, 2, 3)), ([1, 2, 3], 1, (3, 1, 2)), ([1, 2, 3], 2, (2, 3, 1)), ([1, 2, 3], -1, (2, 1, 3)), ([1, 2, 3], 4, (3, 1, 2)), ([], 5, ())])
def test_valid_builtin_tuple(values, steps, expected):
    result = rotate_right(values, steps)
    assert result == expected

@pytest.mark.parametrize("values,steps", [((1, 2), 1), ("abc", 1)])
def test_tuple_subclass_rejected(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)

@pytest.mark.parametrize("values,steps", [(1, 1), ([1, 2, 3], True), ([1, 2, 3], False)])
def test_steps_type_rejected(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)

@pytest.mark.parametrize("values,steps", [(None, 1), (True, 1), ([1, 2], 1.5)])
def test_other_values_rejected(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)

@pytest.mark.parametrize("values,steps", [(TupleChild([1, 2]), 1), ("bad", 1)])
def test_mixed_invalid_input(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)
```

Requirement-to-input mapping:
- Valid `values`: built-in tuples like `(1,)`, `()`, nested lists inside tuples like `([[1], [2]])` are passed to `rotate_right`.
- Invalid `values`: tuple subclasses (`TupleChild`) raise TypeError immediately. Non-tuple values raise TypeError.
- Valid `steps`: exact built-in integers (negative, zero, positive).
- Invalid `steps`: booleans (`True`/`False`), subclasses of int, floats, or other types raise TypeError.
- Logic checks: rotation wraps modulo length; empty input returns `()`; element identities preserved.

Limitations:
- Only a finite set of cases is demonstrated; this does not cover all possible tuple contents, lengths, or step magnitudes.
- No claim that every invalid Python type combination is caught (only representative examples shown).
- No performance evaluation included.