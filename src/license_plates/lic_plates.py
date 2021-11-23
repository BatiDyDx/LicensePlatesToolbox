import re
import random
import itertools
from typing import List, NoReturn, Optional, TypeVar, Union, Match
import operator
import math
import json
import pathlib
from rich.console import Console
from rich.table import Table

# English alphabet
ALPHA: List[str] = [chr(i) for i in range(ord("A"), ord("Z") + 1)]

DIGITS: List[str] = list(map(str, range(0, 10)))


PATH = pathlib.Path(__file__)
with open(PATH.parents[1] / "prog_info.json") as f:
    prog_info = json.load(f)
    STD_PATTERNS = prog_info["License Plates"]["Std Plate Patterns"]


T = TypeVar("T")


class PatternNotValidException(Exception):
    """
    Raised if a pattern is not valid.
    Valid pattern formats contain only C, D or integer characters.
    - "CCCDDC", "3D2C" are valid formats
    - "cccddc", "3d2C" are not valid formats
    """

    def __init__(self, pattern: str) -> None:
        self.msg = f"Pattern {pattern} is not a valid pattern"


class PlateNotValidException(Exception):
    """
    Raised if a license plate is not valid.
    Valid license plates contain only uppercase alphanumerical characters.
    - "FPE405", "4500A" are valid license plates
    - "fpe405", "4500 A" are not valid license plates.
    """

    def __init__(self, plate: str) -> None:
        self.msg = f"Plate {plate} is not a valid license plate"


def value(symb: str) -> int:
    if symb.isdecimal():
        return int(symb)
    return ALPHA.index(symb)


def symbol_by_value(val: int, symbol_type: str) -> str:
    if symbol_type == "D":
        return str(val)
    return ALPHA[val]


def max_plate(pattern: str) -> str:
    """
    Takes a pattern and returns the last plate
    corresponding to the pattern.
    Equivalent to replacing all characters in the pattern
    by Z and digits by 9.
    If pattern is not valid, raises PatternNotValidException
    """
    valid_pattern(pattern)
    pattern = expand_pattern(pattern)
    plate = re.sub("C", "Z", pattern)
    plate = re.sub("D", "9", plate)
    return plate


def min_plate(pattern: str) -> str:
    """
    Takes a pattern and returns the first plate
    corresponding to the pattern.
    Equivalent to replacing all characters in the pattern
    by A and digits by 0.
    If pattern is not valid, raises PatternNotValidException
    """

    plate = re.sub("C", "A", pattern)
    plate = re.sub("D", "0", plate)
    return plate


def combinations(pattern: str) -> int:
    """
    Given a pattern, it returns the number of possible combinations
    that match the pattern.
    If the pattern is not valid, raises PatternNotValidException
    """
    valid_pattern(pattern)
    pattern = expand_pattern(pattern)

    combinations_per_symbol = [len(ALPHA) if s == "C" else len(DIGITS) for s in pattern]
    return math.prod(combinations_per_symbol)


def valid_pattern(pattern: str) -> Union[bool, NoReturn]:
    """
    Checks if the pattern given is valid for a license plate.
    It is equivalent to checking if the pattern contains characters
    other than 'C' and 'D' or integers.
    If the pattern is not valid raises a PatternNotValidException
    """
    valid = re.search(r"[^CD\d]", pattern)
    if valid is not None:
        raise PatternNotValidException(pattern)
    return True


def valid_plate(plate: str) -> Union[bool, NoReturn]:
    """
    Takes a license plate, and checks if its format
    is corect. Returns True if it is, else raises
    PlateNotValidException
    """
    if plate.isalnum() and plate.isupper():
        return True
    raise PlateNotValidException(plate)


def factor_by_position(pattern: str) -> List[int]:
    """
    factor_by_position : str -> List(int)
    Takes a pattern and returns a list, where each element
    is the factor by which each element is multiplied, corresponding
    to the pattern, to get a valid base system
    >>> factor_by_position("DDD")
    [100, 10, 1] # Since its a decimal number, the factors are 10^2, 10^1, 10^0
    >>> factor_by_position("DCD")
    [260, 26, 1]
    """

    valid_pattern(pattern)
    pattern = expand_pattern(pattern)

    # Each element represents the number of possible symbols for each position
    # i.e. if pattern is "CCCDDC", then combinations_per_symbol is
    # [26, 26, 26, 10, 10, 26]
    combinations_per_symbol: List[int] = [
        len(ALPHA) if s == "C" else len(DIGITS) for s in pattern
    ]

    # We get the cumulative product of the list
    pos_factors: List[int] = list(
        itertools.accumulate(combinations_per_symbol[::-1], operator.mul)
    )
    pos_factors = pos_factors[::-1]

    # We take out the first element and append a 1 to the end.
    pos_factors.pop(0)
    pos_factors.append(1)
    return pos_factors


def matches_pattern(pattern: str, plate: str) -> Union[bool, NoReturn]:
    """
    Checks if the plate matches with the pattern given.
    If pattern or plate are not valid, raises PatternNotGivenException
    or PlateNotGivenException respectively.
    >>> matches_pattern("CCDDCC", "FF00DR")
    True
    >>> matches_pattern(ARG_PATTERN_1, "AA123ZX")
    False
    """

    valid_pattern(pattern)
    pattern = expand_pattern(pattern)
    valid_plate(plate)

    if len(plate) != len(pattern):
        return False

    for i, j in zip(plate, pattern):
        if (i.isupper() and j == "C") or (i.isdecimal() and j == "D"):
            continue
        return False
    return True


def repeat_char_n_times(match: Match[str]) -> str:
    """
    Returns the string corresponding to the second element
    matched, repeated as times as the integer value of the first
    element matched.
    """
    return int(match.group(1)) * str(match.group(2))


def expand_pattern(short_pattern: str) -> str:
    """
    Given a pattern in the short form, it returns
    its expanded form.
    If the pattern given is not valid, raises
    a PatternNotValidException
    >>> expand_pattern("3C3D")
    "CCCDDD"
    >>> expand_pattern("3D2CD")
    "DDDCCD"
    """
    valid_pattern(short_pattern)
    pattern = re.sub(r"(\d)([CD])", repeat_char_n_times, short_pattern)
    return pattern


def get_pattern(plate: str) -> Union[str, NoReturn]:
    """
    Given a string that represents a plate, tries to return
    its pattern. If the plate is not valid, raises a
    PlateNotValidException
    """
    valid_plate(plate)
    pattern = re.sub("[A-Z]", "C", plate)
    pattern = re.sub(r"\d", "D", pattern)
    return pattern


def get_plate(pattern: str, n: int) -> str:
    """
    Takes a natural number, and an alphanumerical pattern
    representing the type of the plate, and returns the nth plate.
    If the pattern is not valid, raises PatternNotValidException.
    If n is greater than the number of combinations generated by the pattern
    given, prints a warning and returns max_plate(pattern)
    """

    valid_pattern(pattern)
    pattern = expand_pattern(pattern)
    if n > combinations(pattern):
        console = Console(stderr=True, style="red")
        console.print(
            """WARNING: The input n exceeded the number of
            combinations possible with the pattern given"""
        )
        return max_plate(pattern)

    n -= 1
    position_factors: List[int] = factor_by_position(pattern)
    plate: str = ""

    for i in range(len(pattern)):
        val = n // position_factors[i]
        symbol = symbol_by_value(val, pattern[i])
        plate += symbol
        n %= position_factors[i]

    return plate


def get_plate_index(plate: str) -> Union[int, NoReturn]:
    """
    Takes a string representing a license plate and
    returns its corresponding order number.
    The first license plate of a specific pattern
    will always be 1, and the last one will correspond
    with the number of combinations for its pattern
    >>> get_plate_index("AAA000")
    1
    >>> get_plate_index("AAA001")
    2
    >>> get_plate_index("AA001CD")
    732
    """
    pattern = get_pattern(plate)
    position_factors = factor_by_position(pattern)
    n = 1
    for index, symbol in enumerate(plate):
        n += value(symbol) * position_factors[index]
    return n


def generate_random_pattern(length: int = -1) -> str:
    """
    Generates a random license plate pattern. If length is provided,
    the generated pattern will have the length passed, else, its
    length will be a random number between 4 and 8.
    """
    MIN, MAX = 4, 8  # Min and Max lengths if len is not provided
    if length < 0:
        length = random.randint(MIN, MAX)

    pattern: str = "".join(
        ["C" if random.randint(0, 1) else "D" for _ in range(length)]
    )
    return pattern


def generate_random_plate(pattern: Optional[str] = None) -> str:
    """
    Generates a random plate from a given pattern. If pattern
    is not provided, it generates a random pattern from which
    to create the license plate.
    """
    if pattern is None:
        pattern = generate_random_pattern()
    else:
        valid_pattern(pattern)
        pattern = expand_pattern(pattern)

    plate: str = ""

    for symb in pattern:
        if symb == "C":
            plate += random.choice(ALPHA)
        else:
            plate += random.choice(DIGITS)

    return plate


def std_patterns_table() -> None:
    """
    Prints a table with information about the Standard
    License Plate patterns provided in the STD_PATTERNS
    dictionary. For each of the patterns, the table shows
    the number of combinations and generates a random plate
    """
    table = Table(title="Standard License Plate Patterns")

    table.add_column("Ubication", justify="full", style="bold green")
    table.add_column("Pattern", justify="right", style="blue")
    table.add_column("Combinations", justify="right", style="red")
    table.add_column("Random Example", justify="right", style="bold violet")

    for ubication, pattern in STD_PATTERNS.items():
        table.add_row(
            ubication,
            pattern,
            str(combinations(pattern)),
            generate_random_plate(pattern),
        )

    console = Console()
    console.print(table)
