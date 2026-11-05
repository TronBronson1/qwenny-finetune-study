```python
import copy
import pytest
from subject import transpose

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), [], id="v000"),
    pytest.param(([[]],), [], id="v001"),
    pytest.param(([[], []],), [], id="v002"),
    pytest.param(([[1, 2], [3, 4]],), [[1, 3], [2, 4]], id="v003"),
    pytest.param(([[1, 2, 3]],), [[1], [2], [3]], id="v004"),
    pytest.param(([[1], [2], [3]],), [[1, 2, 3]], id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=transpose(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([ListChild([1])],), id="e001"),
    pytest.param(([[True]],), id="e002"),
    pytest.param(([[IntChild(1)]],), id="e003"),
    pytest.param((['x'],), id="e004"),
    pytest.param((None,), id="e005"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        transpose(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([[1], [2, 3]],), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        transpose(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
