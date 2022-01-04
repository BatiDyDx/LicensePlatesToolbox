from typing import Dict
import pytest
from plates.core import *
from plates.__main__ import (
    parser,
    get_help_str,
    main,
    call,
    print_function_usage,
)


def test_get_plate():
    assert get_plate("CCCDDD", 1) == "AAA000"
    assert get_plate("CCDDDCC", combinations("CCDDDCC")) == "ZZ999ZZ"


@pytest.mark.parametrize("plate,index", [("AAA000", 1), ("AA001CD", 732)])
def test_get_plate_index(plate, index):
    assert get_plate_index(plate) == index


@pytest.mark.parametrize(
    "pattern,total_comb",
    [
        ("CCCDDD", 17_576_000),
        ("CCDDDCC", 456_976_000),
        ("CCDD", 67_600),
    ],
)
def test_combinations(pattern, total_comb):
    assert combinations(pattern) == total_comb


def test_max_plate():
    assert max_plate(STD_PATTERNS["AR-2"]) == "ZZ999ZZ"
    assert max_plate("CCCDDDCCC") == "ZZZ999ZZZ"


def test_min_plate():
    assert min_plate(STD_PATTERNS["AR-1"]) == "AAA000"
    assert min_plate("CCDDCC") == "AA00AA"


@pytest.mark.parametrize("symb,val", [("1", 1), ("A", 0), ("F", 5)])
def test_value(symb, val):
    assert value(symb) == val


@pytest.mark.parametrize(
    "value,value_type,symb", [(9, "D", "9"), (3, "C", "D"), (15, "C", "P")]
)
def test_symbol_by_value(value, value_type, symb):
    assert symbol_by_value(value, value_type) == symb


def test_valid_pattern():
    assert valid_pattern(STD_PATTERNS["AR-1"])
    assert valid_pattern("3C4D")
    assert valid_pattern("3C3D")
    assert not valid_pattern("cDDDCC")
    assert not valid_pattern("4D2CA")


def test_valid_plate():
    assert valid_plate("ABC123")
    assert valid_plate("AA00")
    assert not valid_plate("abc012")
    assert not valid_plate("ABC 777")


def test_factor_by_position():
    assert factor_by_position(STD_PATTERNS["AR-2"]) == [
        26 ** 3 * 1000,
        26 ** 2 * 1000,
        26 ** 2 * 100,
        26 ** 2 * 10,
        26 ** 2,
        26,
        1,
    ]
    assert factor_by_position("CCDDCD") == [
        26 ** 2 * 1000,
        26 * 1000,
        26 * 100,
        26 * 10,
        10,
        1,
    ]


def test_matches_pattern():
    assert matches_pattern(STD_PATTERNS["AR-1"], "PBE370")
    assert matches_pattern(STD_PATTERNS["AR-2"], "AD077YI")
    assert not matches_pattern(STD_PATTERNS["AR-2"], "HGV057")


def test_expand_pattern():
    assert expand_pattern("3C3D") == STD_PATTERNS["AR-1"]
    assert expand_pattern("2C3D2C") == STD_PATTERNS["AR-2"]
    assert expand_pattern(STD_PATTERNS["AR-1"]) == STD_PATTERNS["AR-1"]


def test_get_pattern():
    assert get_pattern("AVG405DF") == "CCCDDDCC"
    assert get_pattern("GVP918") == STD_PATTERNS["AR-1"]
    assert get_pattern("90AKLH") != "DCCCC"


def test_generate_random_plate():
    assert matches_pattern(
        STD_PATTERNS["US-FL"], generate_random_plate(STD_PATTERNS["US-FL"])
    )
    assert valid_plate(generate_random_plate())


def test_generate_random_pattern():
    assert len(generate_random_pattern(6)) == 6
    assert valid_pattern(generate_random_pattern())
    pattern = generate_random_pattern()
    assert matches_pattern(pattern, generate_random_plate(pattern))


def test_main(capture_stdout):
    args = vars(parser.parse_args(["max_plate", "3C3D"]))
    main(args)
    assert "".join(capture_stdout) == max_plate("3C3D") + "\n"

    ##########################
    # Empty the patched stdout
    capture_stdout.clear()
    ##########################

    args = vars(
        parser.parse_args(
            ["matches_pattern", "DF088RE", "--pattern", STD_PATTERNS["AR-2"]]
        )
    )
    main(args)
    assert "".join(capture_stdout) == "True\n"

    with pytest.raises(NotImplementedError):
        args = vars(parser.parse_args(["factor_by_position", "CCCDDD"]))
        main(args)


def test_get_help_str():
    def function(a: str, b: int, c: float) -> str:
        return a * int(c // b)

    assert get_help_str(function) == "\t- function: <a (str)> <b (int)> <c (float)>"


def test_print_function_usage(capture_stdout):
    function_list = ["max_plate", "matches_pattern"]
    max_plate_usage = "- max_plate: <pattern (str)>"
    matches_pattern_usage = "- matches_pattern: <pattern (str)> <plate (str)>"
    print_function_usage(function_list)
    assert (
        "".join(capture_stdout) == f"\t{max_plate_usage}\n\t{matches_pattern_usage}\n"
    )


def test_call():
    def function(x: str, y: str, z: str) -> Dict[str, int]:
        return {x: 1, y: 2, z: 3}

    args = ("b",)
    kwargs = {"x": "a", "z": "c"}

    assert call(function, *args, **kwargs) == {"a": 1, "b": 2, "c": 3}

    with pytest.raises(TypeError):
        call(function, 1, 2, w=3)  # Incorrect keyword argument w

        # More args than parameters passed to function
        call(function, 1, 2, 3, x=2)

        # Less args than parameters passed to function
        call(function, y=2, x=4)
