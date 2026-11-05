```python
import copy
import pytest
from subject import adjacent_equal_count

class IntChild(int): pass
class StrChild(str): pass
class BytesChild(bytes): pass
class ListChild(list): pass
class TupleChild(tuple): pass
class DictChild(dict): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected,after", [
    pytest.param(([],), 0, ([],), id="v000"),
    pytest.param(([1],), 0, ([1],), id="v001"),
    pytest.param(([1, 1],), 1, ([1, 1],), id="v002"),
    pytest.param(([1, 1, 1],), 2, ([1, 1, 1],), id="v003"),
    pytest.param(([1, 2, 1],), 0, ([1, 2, 1],), id="v004"),
    pytest.param(([1, 1, 2, 2, 2],), 3, ([1, 1, 2, 2, 2],), id="v005"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=adjacent_equal_count(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([True],), id="e001"),
    pytest.param(([IntChild(1)],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        adjacent_equal_count(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
