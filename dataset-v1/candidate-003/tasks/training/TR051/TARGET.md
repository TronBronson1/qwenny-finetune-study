```python
import copy
import pytest
from subject import wrap_index

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
    pytest.param((0, 1), 0, (0, 1), id="v000"),
    pytest.param((3, 3), 0, (3, 3), id="v001"),
    pytest.param((-1, 3), 2, (-1, 3), id="v002"),
    pytest.param((-4, 3), 2, (-4, 3), id="v003"),
    pytest.param((8, 3), 2, (8, 3), id="v004"),
    pytest.param((100000000000000000000, 7), 2, (100000000000000000000, 7), id="v005"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=wrap_index(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True, 1), id="e000"),
    pytest.param((IntChild(0), 1), id="e001"),
    pytest.param((1.5, 1), id="e002"),
    pytest.param(('bad', 1), id="e003"),
    pytest.param((None, 1), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(1)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
    pytest.param((True, 0), id="e012"),
    pytest.param((True, -1), id="e013"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        wrap_index(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0), id="e010"),
    pytest.param((0, -1), id="e011"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        wrap_index(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
