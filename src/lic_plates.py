import re
import itertools
from typing import Callable, List, NoReturn, TypeVar, Union, Match
import operator
import math
from functools import wraps
from logging import warning
import json
import pathlib

# English alphabet
ALPHA: List[str] = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

DIGITS: List[int] = list(range(0,10))


PATH = pathlib.Path(__file__)
with open(PATH.parent / "prog_info.json") as f:
    prog_info = json.load(f)
    STD_PATTERNS = prog_info["License Plates"]["Std Plate Patterns"]


T = TypeVar('T')


class PatternNotValidException(Exception):
    def __init__(self, pattern: str) -> None:
        self.msg = f"Pattern {pattern} is not a valid pattern"


class PlateNotValidException(Exception):
    def __init__(self, plate: str) -> None:
        self.msg = f"Plate {plate} is not a valid license plate"


def expand_and_check_pattern(func: Callable[..., T]) -> Callable[..., Union[NoReturn, T]]:
    """
    Takes a function that receives as first parameter a pattern, checks if it is
    valid, expands it if it's a shortened pattern and then executes func with the arguments passed
    """
    @wraps(func)
    def wrapper(pattern: str, *args: Union[int, str], **kwargs: Union[int, str]) -> Union[NoReturn, T]:
        valid_pattern(pattern)
        pattern = expand_pattern(pattern)
        return func(pattern, *args, **kwargs)
    return wrapper


def value(symb: str) -> int:
    if symb.isdecimal():
        return int(symb)
    return ALPHA.index(symb)


def symbol_by_value(val: int, symbol_type: str) -> str:
    if symbol_type == 'D':
        return str(val)
    return ALPHA[val]


@expand_and_check_pattern
def max_plate(pattern: str) -> str:
    plate = re.sub("C", "Z", pattern)
    plate = re.sub("D", "9", plate)
    return plate


@expand_and_check_pattern
def min_plate(pattern: str) -> str:
    plate = re.sub("C", "A", pattern)
    plate = re.sub("D", "0", plate)
    return plate


@expand_and_check_pattern
def combinations(pattern: str) -> int:
    """
    Given a pattern, it returns the number of possible combinations
    that match the pattern
    """
    combinations_per_symbol = [len(ALPHA) if s == 'C' else len(DIGITS) for s in pattern]
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
    if plate.isalnum() and plate.isupper():
        return True
    raise PlateNotValidException(plate)


@expand_and_check_pattern
def factor_by_position(pattern: str) -> List[int]:
    """
    factor_by_position : str -> List(int)
    Takes a pattern and returns a list, where each element
    is the factor by which each element is multiplied, corresponding
    to the pattern, to get a valid base system
    >>> factor_by_position("DDD")
    [100, 10, 1] # Since its a decimal number, the factors are 10^2, 10^1, 10^0
    >>> factor_by_position("DCD")
    [260, 26, 1] # if ESPAÑOL == False
    """
    # Each element represents the number of possible symbols for each position
    # i.e. if pattern is "CCCDDC", then combinations_per_symbol is [26, 26, 26, 10, 10, 26] (only if ESPAÑOL == False)
    combinations_per_symbol: List[int] = [len(ALPHA) if s == 'C' else len(DIGITS) for s in pattern]
    
    # We get the cumulative product of the list
    pos_factors: List[int] = list(itertools.accumulate(combinations_per_symbol[::-1], operator.mul))
    pos_factors = pos_factors[::-1]
    
    # We take out the first element and append a 1 to the end.
    pos_factors.pop(0)
    pos_factors.append(1)
    return pos_factors


@expand_and_check_pattern
def matches_pattern(pattern: str, plate: str) -> Union[bool, NoReturn]:
    """
    Checks if the plate matches with the pattern given
    >>> matches_pattern("CCDDCC", "FF00DR")
    True
    >>> matches_pattern(ARG_PATTERN_1, "AA123ZX")
    False
    """
    valid_plate(plate)

    if len(plate) != len(pattern):
        return False
    
    for i, j in zip(plate, pattern):
        if (i.isupper() and j == 'C') or (i.isdecimal() and j == 'D'):
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
    its expanded form
    >>> expand_pattern("3C3D")
    "CCCDDD"
    >>> expand_pattern("3D2CD")
    "DDDCCD"
    """
    pattern = re.sub(r"(\d)([CD])", repeat_char_n_times, short_pattern)
    return pattern


def get_pattern(plate: str) -> Union[str, NoReturn]:
    valid_plate(plate)
    pattern = re.sub("[A-Z]", "C", plate)
    pattern = re.sub(r"\d", "D", pattern)
    return pattern


@expand_and_check_pattern
def get_plate(pattern: str, n: int) -> str:
    """
    Takes a natural number, and an alphanumerical pattern
    representing the type of the plate, and returns the nth plate.
    """
    if n > combinations(pattern):
        warning("The input n exceeded the number of combinations possible with the pattern given")
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
    """Toma un string que representa una patente, y devuelve el numero de patente correspondiente
    Takes a string representing a license plate and returns its corresponding number.
    >>> get_plate_index("AAA000")
    0
    >>> get_plate_index("AA001CD")
    787
    """
    pattern = get_pattern(plate)
    position_factors = factor_by_position(pattern)
    n = 1
    for index, symbol in enumerate(plate):
        n += value(symbol) * position_factors[index]
    return n
