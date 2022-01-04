import configparser as _configparser
import pathlib as _pathlib

_parser = _configparser.ConfigParser()
_parser.read(_pathlib.Path(__file__).parents[1] / "setup.cfg")
__version__ = _parser.get("metadata", "version")

from .core import (
    combinations,
    expand_pattern,
    generate_random_pattern,
    generate_random_plate,
    get_pattern,
    get_plate,
    get_plate_index,
    matches_pattern,
    max_plate,
    min_plate,
    STD_PATTERNS,
    std_patterns_table,
    valid_pattern,
    valid_plate,
)
