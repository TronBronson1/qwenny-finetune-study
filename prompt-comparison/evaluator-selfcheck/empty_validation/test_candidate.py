import pytest
from rotation import rotate_right
class TupleChild(tuple): pass
class IntChild(int): pass
@pytest.mark.parametrize("values,steps,expected", [((),3,()), ((1,),-9,(1,)), ((1,2,3),0,(1,2,3)), ((1,2,3),1,(3,1,2)), ((1,2,3),-1,(2,3,1)), ((1,2,3),7,(3,1,2)), ((1,1,2),1,(2,1,1))])
def test_returns(values,steps,expected):
    assert rotate_right(values,steps) == expected
    assert type(rotate_right(values,steps)) is tuple
@pytest.mark.parametrize("values,steps", [([],1), (None,1), (TupleChild((1,2)),1), ((1,2),True), ((1,2),False), ((1,2),IntChild(1)), ((1,2),1.5), ((1,2),"1"), ((1,2),None), ((),True)])
def test_types(values,steps):
    with pytest.raises(TypeError): rotate_right(values,steps)
def test_identity_and_mutation():
    a,b = [1], {"x":2}
    result = rotate_right((a,b),1)
    assert result[0] is b and result[1] is a
    assert a == [1] and b == {"x":2}
