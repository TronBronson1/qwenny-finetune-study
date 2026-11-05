import copy
import pytest
from subject import parse_range

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
    pytest.param(('[0:0]',), (0, 0), ('[0:0]',), id="v000"),
    pytest.param(('[0:99]',), (0, 99), ('[0:99]',), id="v001"),
    pytest.param(('[3:7]',), (3, 7), ('[3:7]',), id="v002"),
    pytest.param(('[99:99]',), (99, 99), ('[99:99]',), id="v003"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=parse_range(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('[0:0]'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_range(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('[7:3]',), id="e004"),
    pytest.param(('0:1',), id="e005"),
    pytest.param(('[00:1]',), id="e006"),
    pytest.param(('[0:100]',), id="e007"),
    pytest.param(('[0:1] ',), id="e008"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_range(*args)
