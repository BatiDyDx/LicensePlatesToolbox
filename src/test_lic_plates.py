from .lic_plates import *
import pytest

def test_get_plate():
    assert get_plate("CCCDDD", 1) == "AAA000"
    assert get_plate("CCDDDCC", combinations("CCDDDCC")) == "ZZ999ZZ"


def test_get_plate_index():
    assert get_plate_index("AAA000") == 1
    assert get_plate_index("AA001CD") == 732


def test_combinations():
    assert combinations(STD_PATTERNS["ARG_1"]) == 17_576_000
    assert combinations(STD_PATTERNS["ARG_2"]) == 456_976_000
    assert combinations("CCDD") == 67_600


def test_max_plate():
    assert max_plate(STD_PATTERNS["ARG_2"]) == "ZZ999ZZ"
    assert max_plate("CCCDDDCCC") == "ZZZ999ZZZ"


def test_min_plate():
    assert min_plate(STD_PATTERNS["ARG_1"]) == "AAA000"
    assert min_plate("CCDDCC") == "AA00AA"


def test_value():
    assert value('1') == 1
    assert value('A') == 0
    assert value('F') == 5


def test_symbol_by_value():
    assert symbol_by_value(9, 'D') == '9'
    assert symbol_by_value(3, 'C') == 'D'
    assert symbol_by_value(15, 'C') == 'P'


def test_valid_pattern():
    assert valid_pattern(STD_PATTERNS["ARG_1"])
    assert valid_pattern("3C4D")
    with pytest.raises(PatternNotValidException):
        valid_pattern("cDDDCC")
        valid_pattern("4D2CA")


def test_valid_plate():
    assert valid_plate("ABC123")
    assert valid_plate("AA00")
    assert valid_pattern("3C3D")
    with pytest.raises(PlateNotValidException):
        valid_plate("abc012")
        valid_plate("ABC 777")


def test_factor_by_position():
    assert factor_by_position(STD_PATTERNS["ARG_2"]) == [
        26 ** 3 * 1000, 
        26 ** 2 * 1000,
        26 ** 2 * 100,
        26 ** 2 * 10,
        26 ** 2,
        26, 
        1
    ]
    assert factor_by_position("CCDDCD") == [
        26 ** 2 * 1000,
        26 * 1000,
        26 * 100,
        26 * 10,
        10,
        1
    ]


def test_matches_pattern():
    assert matches_pattern(STD_PATTERNS["ARG_1"], "PBE370")
    assert matches_pattern(STD_PATTERNS["ARG_2"], "AD077YI")
    assert not matches_pattern(STD_PATTERNS["ARG_2"], "HGV057")


def test_expand_pattern():
    assert expand_pattern("3C3D") == STD_PATTERNS["ARG_1"]
    assert expand_pattern("2C3D2C") == STD_PATTERNS["ARG_2"]
    assert expand_pattern(STD_PATTERNS["ARG_1"]) == STD_PATTERNS["ARG_1"]


def test_get_pattern():
    assert get_pattern("AVG405DF") == "CCCDDDCC"
    assert get_pattern("GVP918") == STD_PATTERNS["ARG_1"]
    assert get_pattern("90AKLH") != "DCCCC"
