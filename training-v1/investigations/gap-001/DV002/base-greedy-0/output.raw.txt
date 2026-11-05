```python
import pytest
from subject import minute_of_day

class TestMinuteOfDay:
    def test_valid_00_00(self):
        assert minute_of_day("00:00") == 0

    def test_valid_12_30(self):
        assert minute_of_day("12:30") == 750

    def test_valid_23_59(self):
        assert minute_of_day("23:59") == 1439

    def test_valid_01_01(self):
        assert minute_of_day("01:01") == 61

    def test_valid_09_45(self):
        assert minute_of_day("09:45") == 585

    def test_valid_15_00(self):
        assert minute_of_day("15:00") == 900

    def test_valid_20_15(self):
        assert minute_of_day("20:15") == 1215

    def test_valid_00_01(self):
        assert minute_of_day("00:01") == 1

    def test_valid_00_59(self):
        assert minute_of_day("00:59") == 59

    def test_valid_01_00(self):
        assert minute_of_day("01:00") == 60

    def test_valid_01_59(self):
        assert minute_of_day("01:59") == 119

    def test_valid_02_00(self):
        assert minute_of_day("02:00") == 120

    def test_valid_02_59(self):
        assert minute_of_day("02:59") == 179

    def test_valid_03_00(self):
        assert minute_of_day("03:00") == 180

    def test_valid_03_59(self):
        assert minute_of_day("03:59") == 239

    def test_valid_04_00(self):
        assert minute_of_day("04:00") == 240

    def test_valid_04_59(self):
        assert minute_of_day("04:59") == 299

    def test_valid_05_00(self):
        assert minute_of_day("05:00") == 300

    def test_valid_05_59(self):
        assert minute_of_day("05:59") == 359

    def test_valid_06_00(self):
        assert minute_of_day("06:00") == 360

    def test_valid_06_59(self):
        assert minute_of_day("06:59") == 419

    def test_valid_07_00(self):
        assert minute_of_day("07:00") == 420

    def test_valid_07_59(self):
        assert minute_of_day("07:59") == 479

    def test_valid_08_00(self):
        assert minute_of_day("08:00") == 480

    def test_valid_08_59(self):
        assert minute_of_day("08:59") == 539

    def test_valid_09_00(self):
        assert minute_of_day("09:00") == 540

    def test_valid_09_59(self):
        assert minute_of_day("09:59") == 599

    def test_valid_10_00(self):
        assert minute_of_day("10:00") == 600

    def test_valid_10_59(self):
        assert minute_of_day("10:59") == 659

    def test_valid_11_00(self):
        assert minute_of_day("11:00") == 660

    def test_valid_11_59(self):
        assert minute_of_day("11:59") == 719

    def test_valid_12_00(self):
        assert minute_of_day("12:00") == 720

    def test_valid_12_59(self):
        assert minute_of_day("12:59") == 779

    def test_valid_13_00(self):
        assert minute_of_day("13:00") == 780

    def test_valid_13_59(self):
        assert minute_of_day("13:59") == 839

    def test_valid_14_00(self):
        assert minute_of_day("14:00") == 840

    def test_valid_14_59(self):
        assert minute_of_day("14:59") == 899

    def test_valid_15_00(self):
        assert minute_of_day("15:00") == 900

    def test_valid_15_59(self):
        assert minute_of_day("15:59") == 959

    def test_valid_16_00(self):
        assert minute_of_day("16:00") == 960

    def test_valid_16_59(self):
        assert minute_of_day("16:59") == 1019

    def test_valid_17_00(self):
        assert minute_of_day("17:00") == 1020

    def test_valid_17_59(self):
        assert minute_of_day("17:59") == 1079

    def test_valid_18_00(self):
        assert minute_of_day("18:00") == 1080

    def test_valid_18_59(self):
        assert minute_of_day("18:59") == 1139

    def test_valid_19_00(self):
        assert minute_of_day("19:00") == 1140

    def test_valid_19_59(self):
        assert minute_of_day("19:59") == 1199

    def test_valid_20_00(self):
        assert minute_of_day("20:00") == 1200

    def test_valid_20_59(self):
        assert minute_of_day("20:59") == 1259

    def test_valid_21_00(self):
        assert minute_of_day("21:00") == 1260

    def test_valid_21_59(self):
        assert minute_of_day("21:59") == 1319

    def test_valid_22_00(self):
        assert minute_of_day("22:00") == 1320

    def test_valid_22_59(self):
        assert minute_of_day("22:59") == 1379

    def test_valid_23_00(self):
        assert minute_of_day("23:00") == 1380

    def test_valid_23_59(self):
        assert minute_of_day("23:59") == 1439

    def test_invalid_hour_24(self):
        with pytest.raises(ValueError):
            minute_of_day("24:00")

    def test_invalid_hour_25(self):
        with pytest.raises(ValueError):
            minute_of_day("25:00")

    def test_invalid_hour_01_59(self):
        with pytest.raises(ValueError):
            minute_of_day("01:59")

    def test_invalid_hour_00_60(self):
        with pytest.raises(ValueError):
            minute_of_day("00:60")

    def test_invalid_hour_00_61(self):
        with pytest.raises(ValueError):
            minute_of_day("00:61")

    def test_invalid_hour_00_99(self):
        with pytest.raises(ValueError):
            minute_of_day("00:99")

    def test_invalid_hour_00_100(self):
        with pytest.raises(ValueError):
            minute_of_day("00:100")

    def test_invalid_hour_00_120(self):
        with pytest.raises(ValueError):
            minute_of_day("00:120")

    def test_invalid_hour_00_1439(self):
        with pytest.raises(ValueError):
            minute_of_day("00:1439")

    def test_invalid_hour_00_1440(self):