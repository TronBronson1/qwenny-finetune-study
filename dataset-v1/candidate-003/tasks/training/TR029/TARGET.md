```python
import copy
import pytest
from subject import chunk_list

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
    pytest.param(([], 2), [], ([], 2), id="v000"),
    pytest.param(([1], 2), [[1]], ([1], 2), id="v001"),
    pytest.param(([1, 2, 3, 4], 2), [[1, 2], [3, 4]], ([1, 2, 3, 4], 2), id="v002"),
    pytest.param(([1, 2, 3], 2), [[1, 2], [3]], ([1, 2, 3], 2), id="v003"),
    pytest.param(([1, 2], 1), [[1], [2]], ([1, 2], 1), id="v004"),
    pytest.param(([1, 2], 9), [[1, 2]], ([1, 2], 9), id="v005"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=chunk_list(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 2), id="e000"),
    pytest.param(([True], 2), id="e001"),
    pytest.param(([IntChild(1)], 2), id="e002"),
    pytest.param(((), 2), id="e003"),
    pytest.param((None, 2), id="e004"),
    pytest.param(([], True), id="e005"),
    pytest.param(([], IntChild(2)), id="e006"),
    pytest.param(([], 1.5), id="e007"),
    pytest.param(([], 'bad'), id="e008"),
    pytest.param(([], None), id="e009"),
    pytest.param((ListChild([]), -1), id="e012"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        chunk_list(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([1], 0), id="e010"),
    pytest.param(([], -1), id="e011"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        chunk_list(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
