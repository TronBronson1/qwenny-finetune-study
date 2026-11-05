```python
import pytest
from subject import parse_version

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('0.0.0',), (0, 0, 0), id="v000"),
    pytest.param(('1.2.3',), (1, 2, 3), id="v001"),
    pytest.param(('999.0.10',), (999, 0, 10), id="v002"),
    pytest.param(('0.999.999',), (0, 999, 999), id="v003"),
])
def test_values(args,expected):
    actual=parse_version(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0.0.0'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('1.2'),), id="e015"),
    pytest.param((StrChild('1.2.3.4'),), id="e016"),
    pytest.param((StrChild('01.2.3'),), id="e017"),
    pytest.param((StrChild('1.2.1000'),), id="e018"),
    pytest.param((StrChild('1.2.٣'),), id="e019"),
    pytest.param((StrChild('١.2.3'),), id="e020"),
    pytest.param((StrChild('1.２.3'),), id="e021"),
    pytest.param((StrChild('0.1000.0'),), id="e022"),
    pytest.param((StrChild('0.0.1000'),), id="e023"),
    pytest.param((StrChild('1٠.0.0'),), id="e024"),
    pytest.param((StrChild('0.0.1٠'),), id="e025"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_version(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('1.2',), id="e004"),
    pytest.param(('1.2.3.4',), id="e005"),
    pytest.param(('01.2.3',), id="e006"),
    pytest.param(('1.2.1000',), id="e007"),
    pytest.param(('1.2.٣',), id="e008"),
    pytest.param(('١.2.3',), id="e009"),
    pytest.param(('1.２.3',), id="e010"),
    pytest.param(('0.1000.0',), id="e011"),
    pytest.param(('0.0.1000',), id="e012"),
    pytest.param(('1٠.0.0',), id="e013"),
    pytest.param(('0.0.1٠',), id="e014"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_version(*args)
```

Return cases: zeros=v000; ordinary=v001; upper-bound=v002; later-components-upper-bound=v003. Validation cases: TypeError=e000,e001,e002,e003,e015,e016,e017,e018,e019,e020,e021,e022,e023,e024,e025; ValueError=e004,e005,e006,e007,e008,e009,e010,e011,e012,e013,e014. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
