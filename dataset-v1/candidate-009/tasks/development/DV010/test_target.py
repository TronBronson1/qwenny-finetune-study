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

@pytest.mark.parametrize("args,expected", [
    pytest.param((['0'],), 0, id="v000"),
    pytest.param((['-0'],), 0, id="v001"),
    pytest.param((['2', '3', '+'],), 5, id="v002"),
    pytest.param((['2', '3', '-'],), -1, id="v003"),
    pytest.param((['2', '3', '4', '*', '+'],), 14, id="v004"),
    pytest.param((['-2', '3', '*'],), -6, id="v005"),
    pytest.param((['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+'],), 16, id="v006"),
    pytest.param((['9999'],), 9999, id="v007"),
    pytest.param((['-9999'],), -9999, id="v008"),
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
    pytest.param((['+', 1],), id="e013"),
    pytest.param((ListChild([]),), id="e016"),
    pytest.param((ListChild(['+']),), id="e017"),
    pytest.param((ListChild(['1', '2']),), id="e018"),
    pytest.param((ListChild(['01']),), id="e019"),
    pytest.param((ListChild(['1', '/']),), id="e020"),
    pytest.param((ListChild(['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']),), id="e021"),
    pytest.param((ListChild(['٣']),), id="e022"),
    pytest.param((ListChild(['３']),), id="e023"),
    pytest.param((ListChild(['10000']),), id="e024"),
    pytest.param((ListChild(['4', '+']),), id="e025"),
])
def test_raises_typeerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(TypeError):
        rpn_evaluate(*args)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(([],), id="e005"),
    pytest.param((['+'],), id="e006"),
    pytest.param((['1', '2'],), id="e007"),
    pytest.param((['01'],), id="e008"),
    pytest.param((['1', '/'],), id="e009"),
    pytest.param((['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],), id="e010"),
    pytest.param((['٣'],), id="e011"),
    pytest.param((['３'],), id="e012"),
    pytest.param((['10000'],), id="e014"),
    pytest.param((['4', '+'],), id="e015"),
])
def test_raises_valueerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(ValueError):
        rpn_evaluate(*args)
    assert args == before
