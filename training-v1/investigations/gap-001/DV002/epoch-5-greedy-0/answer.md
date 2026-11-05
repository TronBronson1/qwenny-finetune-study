```python
import copy
import pytest
from subject import minute_of_day

class StrChild(str): pass

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
    pytest.param( ('00:00',), 0, id="v000" ),
    pytest.param( ('00:01',), 1, id="v001" ),
    pytest.param( ('00:30',), 30, id="v002" ),
    pytest.param( ('00:59',), 59, id="v003" ),
    pytest.param( ('01:00',), 60, id="v004" ),
    pytest.param( ('01:01',), 61, id="v005" ),
    pytest.param( ('01:30',), 90, id="v006" ),
    pytest.param( ('01:59',), 119, id="v007" ),
    pytest.param( ('02:00',), 120, id="v008" ),
    pytest.param( ('02:01',), 121, id="v009" ),
    pytest.param( ('02:30',), 150, id="v010" ),
    pytest.param( ('02:59',), 179, id="v011" ),
    pytest.param( ('03:00',), 180, id="v012" ),
    pytest.param( ('03:01',), 181, id="v013" ),
    pytest.param( ('03:30',), 210, id="v014" ),
    pytest.param( ('03:59',), 239, id="v015" ),
    pytest.param( ('04:00',), 240, id="v016" ),
    pytest.param( ('04:01',), 241, id="v017" ),
    pytest.param( ('04:30',), 270, id="v018" ),
    pytest.param( ('04:59',), 299, id="v019" ),
    pytest.param( ('05:00',), 300, id="v020" ),
    pytest.param( ('05:01',), 301, id="v021" ),
    pytest.param( ('05:30',), 330, id="v022" ),
    pytest.param( ('05:59',), 359, id="v023" ),
    pytest.param( ('06:00',), 360, id="v024" ),
    pytest.param( ('06:01',), 361, id="v025" ),
    pytest.param( ('06:30',), 390, id="v026" ),
    pytest.param( ('06:59',), 419, id="v027" ),
    pytest.param( ('07:00',), 420, id="v028" ),
    pytest.param( ('07:01',), 421, id="v029" ),
    pytest.param( ('07:30',), 450, id="v030" ),
    pytest.param( ('07:59',), 479, id="v031" ),
    pytest.param( ('08:00',), 480, id="v032" ),
    pytest.param( ('08:01',), 481, id="v033" ),
    pytest.param( ('08:30',), 510, id="v034" ),
    pytest.param( ('08:59',), 539, id="v035" ),
    pytest.param( ('09:00',), 540, id="v036" ),
    pytest.param( ('09:01',), 541, id="v037" ),
    pytest.param( ('09:30',), 570, id="v038" ),
    pytest.param( ('09:59',), 599, id="v039" ),
    pytest.param( ('10:00',), 600, id="v040" ),
    pytest.param( ('10:01',), 601, id="v041" ),
    pytest.param( ('10:30',), 630, id="v042" ),
    pytest.param( ('10:59',), 659, id="v043" ),
    pytest.param( ('11:00',), 660, id="v044" ),
    pytest.param( ('11:01',), 661, id="v045" ),
    pytest.param( ('11:30',), 690, id="v046" ),
    pytest.param( ('11:59',), 719, id="v047" ),
    pytest.param( ('12:00',), 720, id="v048" ),
    pytest.param( ('12:01',), 721, id="v049" ),
    pytest.param( ('12:30',), 750, id="v050" ),
    pytest.param( ('12:59',), 779, id="v051" ),
    pytest.param( ('13:00',), 780, id="v052" ),
    pytest.param( ('13:01',), 781, id="v053" ),
    pytest.param( ('13:30',), 810, id="v054" ),
    pytest.param( ('13:59',), 839, id="v055" ),
    pytest.param( ('14:00',), 840, id="v056" ),
    pytest.param( ('14:01',), 841, id="v057" ),
    pytest.param( ('14:30',), 870, id="v058" ),
    pytest.param( ('14:59',), 899, id="v059" ),
    pytest.param( ('15:00',), 900, id="v060" ),
    pytest.param( ('15:01',), 901, id="v061" ),
    pytest.param( ('15:30',), 930, id="v062" ),
    pytest.param( ('15:59',), 959, id="v063" ),
    pytest.param( ('16:00',), 960, id="v064" ),
    pytest.param( ('16:01',), 961, id="v065" ),
    pytest.param( ('16:30',), 990, id="v066" ),
    pytest.param( ('16:59',), 1019, id="v067" ),
    pytest.param( ('17:00',), 1020, id="v068" ),
    pytest.param( ('17:01',), 1021, id="v069" ),
    pytest.param( ('17:30',), 1050, id="v070" ),
    pytest.param( ('17:59',), 1079, id="v071" ),
    pytest.param( ('18:00',), 1080, id="v072" ),
    pytest.param( ('18:01',), 