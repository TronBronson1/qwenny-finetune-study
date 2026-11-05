import pytest
from batch_count import batches

class IntChild(int):
    pass

class StrChild(str):
    pass

@pytest.mark.parametrize("left,right,expected", [(0, 3, 0), (1, 3, 1), (3, 3, 1), (4, 3, 2), (7, 1, 7), (10**30, 3, 333333333333333333333333333334)])
def test_returns(left, right, expected):
    assert batches(left, right) == expected

@pytest.mark.parametrize("left,right", [(True, 3), (False, 3), (IntChild(2), 3), (1.5, 3), ("2", 3), (None, 3), (2, True), (2, False), (2, IntChild(3)), (2, 1.5), (2, "3"), (2, None)])
def test_types(left, right):
    with pytest.raises(TypeError):
        batches(left, right)

@pytest.mark.parametrize("left,right", [(-1, 3), (2, 0), (2, -1)])
def test_values(left, right):
    with pytest.raises(ValueError):
        batches(left, right)

@pytest.mark.parametrize("left,right", [("bad", 0), (-1, "bad")])
def test_type_precedence(left, right):
    with pytest.raises(TypeError):
        batches(left, right)
