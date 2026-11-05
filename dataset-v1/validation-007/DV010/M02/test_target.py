import copy
import pytest
from subject import rpn_evaluate

class StrChild(str): pass
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
    pytest.param((['0'],), 0, id="v000"),
    pytest.param((['-0'],), 0, id="v001"),
    pytest.param((['2', '3', '+'],), 5, id="v002"),
    pytest.param((['2', '3', '-'],), -1, id="v003"),
    pytest.param((['2', '3', '4', '*', '+'],), 14, id="v004"),
    pytest.param((['-2', '3', '*'],), -6, id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=rpn_evaluate(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild(['0']),), id="e000"),
    pytest.param(([StrChild('x')],), id="e001"),
    pytest.param(([1],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((ListChild([]),), id="e011"),
    pytest.param((ListChild(['+']),), id="e012"),
    pytest.param((ListChild(['1', '2']),), id="e013"),
    pytest.param((ListChild(['01']),), id="e014"),
    pytest.param((ListChild(['1', '/']),), id="e015"),
    pytest.param((ListChild(['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']),), id="e016"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        rpn_evaluate(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([],), id="e005"),
    pytest.param((['+'],), id="e006"),
    pytest.param((['1', '2'],), id="e007"),
    pytest.param((['01'],), id="e008"),
    pytest.param((['1', '/'],), id="e009"),
    pytest.param((['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],), id="e010"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        rpn_evaluate(*args)
