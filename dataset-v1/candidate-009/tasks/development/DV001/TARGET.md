```python
import copy
import pytest
from subject import rotate_right

class IntChild(int): pass
class TupleChild(tuple): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(((), 0), (), id="v000"),
    pytest.param(((), 4), (), id="v001"),
    pytest.param(((1,), -9), (1,), id="v002"),
    pytest.param(((1, 2, 3), 0), (1, 2, 3), id="v003"),
    pytest.param(((1, 2, 3), 1), (3, 1, 2), id="v004"),
    pytest.param(((1, 2, 3), -1), (2, 3, 1), id="v005"),
    pytest.param(((1, 2, 3), 7), (3, 1, 2), id="v006"),
    pytest.param(((1, 1, 2), 2), (1, 2, 1), id="v007"),
    pytest.param((([1], {'k': 2}), 1), ({'k': 2}, [1]), id="v008"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=rotate_right(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((TupleChild(()), 0), id="e000"),
    pytest.param(([], 0), id="e001"),
    pytest.param((None, 0), id="e002"),
    pytest.param(((), True), id="e003"),
    pytest.param(((), IntChild(0)), id="e004"),
    pytest.param(((), 1.5), id="e005"),
    pytest.param(((), 'bad'), id="e006"),
    pytest.param(((), None), id="e007"),
])
def test_raises_typeerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(TypeError):
        rotate_right(*args)
    assert args == before

def test_identity_and_no_element_mutation():
    first=[1]
    second={"k":2}
    third=object()
    values=(first,second,third)
    result=rotate_right(values,1)
    assert type(result) is tuple
    assert result[0] is third
    assert result[1] is first
    assert result[2] is second
    assert first == [1]
    assert second == {"k":2}
```

Return cases: empty-zero=v000; empty-positive=v001; single-negative=v002; identity=v003; right=v004; left=v005; wrap=v006; duplicates=v007; mutable-elements=v008. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007. Exact returned types are checked recursively where specified. Input preservation is checked before/after every call, including expected-exception calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
