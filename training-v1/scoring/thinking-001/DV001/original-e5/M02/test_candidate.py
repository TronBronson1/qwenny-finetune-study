import copy
import pytest
from subject import rotate_right

class MyTuple(tuple):
    pass

class MyInt(int):
    pass

class MyList(list):
    pass

TEST_RETURN_VALUES = [
    ((1,), 1), (1,),
    ((0, 1, 2), 1), (2, 0, 1),
    ((1, 2, 3), -1), (2, 3, 1),
    ((1, 2, 3), 4), (2, 3, 1),
    ((1, 2, 3), 3), (1, 2, 3),
    ((1,), 0), (1,),
    ((nested, ), None),
]

TEST_RETURN_EXCEPTIONS = [
    ((1,), 1),
    ((0, 1, 2), 1),
    ((1, 2, 3), -1),
    ((1, 2, 3), 4),
    ((1, 2, 3), 3),
    ((1,), 0),
    ((1,), None),
]

@pytest.mark.parametrize("values,expected", TEST_RETURN_VALUES)
def test_values(values, expected):
    actual = rotate_right(*values)
    assert actual is expected

@pytest.mark.parametrize("values,exception", TEST_RETURN_EXCEPTIONS)
def test_raises(values, exception):
    with pytest.raises(exception):
        rotate_right(*values)
