```python
import pytest
from subject import index_of_nth

class IntChild(int): pass
class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('', 'a', 1), -1, id="v000"),
    pytest.param(('aaaa', 'aa', 1), 0, id="v001"),
    pytest.param(('aaaa', 'aa', 2), 1, id="v002"),
    pytest.param(('aaaa', 'aa', 3), 2, id="v003"),
    pytest.param(('aaaa', 'aa', 4), -1, id="v004"),
    pytest.param(('abc', 'abc', 1), 0, id="v005"),
    pytest.param(('abc', 'x', 1), -1, id="v006"),
    pytest.param(('éé', 'é', 2), 1, id="v007"),
    pytest.param(('Aa', 'a', 1), 1, id="v008"),
    pytest.param(('aA', 'a', 2), -1, id="v009"),
])
def test_values(args,expected):
    actual=index_of_nth(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''), 'a', 1), id="e000"),
    pytest.param((b'x', 'a', 1), id="e001"),
    pytest.param((1, 'a', 1), id="e002"),
    pytest.param((None, 'a', 1), id="e003"),
    pytest.param(('', StrChild('a'), 1), id="e004"),
    pytest.param(('', b'x', 1), id="e005"),
    pytest.param(('', 1, 1), id="e006"),
    pytest.param(('', None, 1), id="e007"),
    pytest.param(('', 'a', True), id="e008"),
    pytest.param(('', 'a', IntChild(1)), id="e009"),
    pytest.param(('', 'a', 1.5), id="e010"),
    pytest.param(('', 'a', 'bad'), id="e011"),
    pytest.param(('', 'a', None), id="e012"),
    pytest.param((StrChild('abc'), '', 1), id="e015"),
    pytest.param(('abc', StrChild(''), 1), id="e016"),
    pytest.param(('abc', '', IntChild(1)), id="e017"),
    pytest.param((StrChild('abc'), 'a', 0), id="e018"),
    pytest.param(('abc', StrChild('a'), 0), id="e019"),
    pytest.param(('abc', 'a', IntChild(0)), id="e020"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        index_of_nth(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('abc', '', 1), id="e013"),
    pytest.param(('abc', 'a', 0), id="e014"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        index_of_nth(*args)
```

Return cases: empty=v000; first-overlap=v001; second-overlap=v002; third-overlap=v003; missing-overlap=v004; whole-string=v005; absent=v006; unicode=v007; literal-case=v008; no-second-case-match=v009. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e010,e011,e012,e015,e016,e017,e018,e019,e020; ValueError=e013,e014. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
