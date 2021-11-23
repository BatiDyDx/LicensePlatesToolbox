__version__ = "1.0"

from lic_plates import (
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
    valid_plate
)

__all__ = [
    "combinations", "expand_pattern", "factor_by_position", 
    "generate_random_pattern", "generate_random_plate", "get_pattern",
    "get_plate", "get_plate_index", "matches_pattern", "max_plate", 
    "min_plate", "PatternNotValidException", "PlateNotValidException",
    "STD_PATTERNS", "std_patterns_table", "symbol_by_value", 
    "valid_pattern", "valid_plate", "value" 
]