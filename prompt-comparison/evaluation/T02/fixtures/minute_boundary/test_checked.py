import pytest
from clock_parser import minute_of_day
class StrChild(str): pass
@pytest.mark.parametrize("text,expected", [("00:00",0),("23:59",1439),("12:34",754),("01:00",60),("00:01",1)])
def test_returns(text,expected):
    result=minute_of_day(text)
    assert result == expected and type(result) is int
@pytest.mark.parametrize("text", ["24:00","23:60","99:00","00:99","1:02","01:2","01-02","01:020",""," 01:02","01:02 ","+1:02","01:-2","０１:０２","٠١:٠٢","aa:bb"])
def test_values(text):
    with pytest.raises(ValueError): minute_of_day(text)
@pytest.mark.parametrize("text", [True,False,1,1.5,None,b"01:02",StrChild("01:02")])
def test_types(text):
    with pytest.raises(TypeError): minute_of_day(text)
