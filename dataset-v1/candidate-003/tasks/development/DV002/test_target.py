import copy
import pytest
from subject import minute_of_day

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
    pytest.param(('00:00',), 0, ('00:00',), id="v000"),
    pytest.param(('00:01',), 1, ('00:01',), id="v001"),
    pytest.param(('01:00',), 60, ('01:00',), id="v002"),
    pytest.param(('12:34',), 754, ('12:34',), id="v003"),
    pytest.param(('23:59',), 1439, ('23:59',), id="v004"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=minute_of_day(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('00:00'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        minute_of_day(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('24:00',), id="e004"),
    pytest.param(('23:60',), id="e005"),
    pytest.param(('1:00',), id="e006"),
    pytest.param(('00:0',), id="e007"),
    pytest.param(('00-00',), id="e008"),
    pytest.param((' 00:00',), id="e009"),
    pytest.param(('00:00\n',), id="e010"),
    pytest.param(('٠٠:٠٠',), id="e011"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        minute_of_day(*args)
