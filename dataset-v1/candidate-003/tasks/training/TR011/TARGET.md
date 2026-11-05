```python
import copy
import pytest
from subject import leap_year

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
    pytest.param((1,), False, (1,), id="v000"),
    pytest.param((4,), True, (4,), id="v001"),
    pytest.param((1900,), False, (1900,), id="v002"),
    pytest.param((2000,), True, (2000,), id="v003"),
    pytest.param((2023,), False, (2023,), id="v004"),
    pytest.param((2024,), True, (2024,), id="v005"),
    pytest.param((2100,), False, (2100,), id="v006"),
    pytest.param((9999,), False, (9999,), id="v007"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=leap_year(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(1),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        leap_year(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0,), id="e005"),
    pytest.param((10000,), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        leap_year(*args)
```

Explicit return/post-state cases v000–v007 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
