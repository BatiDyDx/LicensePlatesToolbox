import argparse
import json
import pathlib
from typing import Any, Callable, Dict, Iterable, List, Mapping, Union

from plates import __version__ as __version__
from plates import core


PATH = pathlib.Path(__file__)

with open(PATH.parent / "data.json") as f:
    json_file = json.loads(f.read())

programme_info = json_file["License Plates"]["Programme Info"]
USAGE: str = programme_info["Programme Usage"]
DESCRIPTION: str = programme_info["Programme Description"]
EPILOG: str = programme_info["Programme Epilog"]


FUNCTION_NAMES: List[str] = [
    "combinations",
    "get_plate_index",
    "get_plate",
    "matches_pattern",
    "get_pattern",
    "max_plate",
    "min_plate",
    "std_patterns_table",
]

# Create parser for command line arguments
parser = argparse.ArgumentParser(
    prog="plates",
    usage=USAGE,
    description=DESCRIPTION,
    add_help=True,
    epilog=EPILOG,
)

parser.add_argument(
    dest="args",
    nargs="*",
)

parser.add_argument(
    "-p",
    "--pattern",
    dest="pattern",
    action="store",
    type=str,
)

parser.add_argument(
    "-pl",
    "--plate",
    dest="plate",
    action="store",
    type=str,
)

parser.add_argument(
    "-i",
    "--index",
    dest="index",
    action="store",
    type=int,
)

parser.add_argument(
    "-lf",
    "--list-functions",
    dest="list_functions",
    action="store_true",
    help="shows a list of available functions"
    "with its parameters and corresponding types",
)

parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s version: {__version__}"
)


def print_function_usage(function_list: Iterable[str]) -> None:
    """
    Prints the string returned by get_help_str for each function in the list
    """
    for func_name in function_list:
        func: Callable[..., Any] = getattr(core, func_name)
        print(get_help_str(func))


def get_help_str(f: Callable[..., Any]) -> str:
    """
    Returns a string with format:
        - (function_name): <args (arg_type)> ...
    If f takes no argument, then the string returned is:
        - (function_name): (no args)
    """
    parameters: Dict[str, type] = f.__annotations__.copy()
    del parameters["return"]
    help_str: str = f"\t- {f.__name__}:"
    if not parameters:
        help_str += " (no args)"
    else:
        for pname, ptype in parameters.items():
            help_str += f" <{pname} ({ptype.__name__})>"
    return help_str


def call(f: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    For each parameter that f takes, it is looked up in the kwargs,
    if present, then passed to f, otherwise the following argument is
    consumed starting from the first one.
    Example:
    Take the following function
    def add(x, y, z):
        return x + 2*y + 10*z
    Then:
    >>> call(add, 5, 3, y = 1)
    37
    In this example, call first looks for x in kwargs. x is not found,
    so the first positional argument, 5, is assigned to x. Then y is
    assigned to 1 as it was passed as a keyword argument. Finally, z
    is not a keyword argument, so it is consumed from the following
    positional argument, in this case 3. Then, the call to add looks like
    add(5, 1, 3) which returns 37.
    """
    params: Dict[str, type] = f.__annotations__.copy()
    # return is not a parameter so we take it out
    params.pop("return", None)

    if len(args) + len(kwargs) != len(params):
        raise TypeError(
            "Incorrect number of arguments passed. "
            f"Required number of arguments is {len(params)}, "
            f"but {len(args) + len(kwargs)} were passed"
        )

    for key in kwargs:
        # If an incorrect keyword argument was passed,
        # an error is raised
        if key not in params:
            raise TypeError(
                f"Keyword argument {key} was passed but not used in the function."
            )

    for pname, ptype in params.items():
        # If the parameter wasnt passed as keyword, then
        # it is consumed from args and correctly casted
        # according to the function signature
        if kwargs.get(pname, None) is None:
            kwargs[pname] = ptype(args[0])
            args = args[1:]

    return f(**kwargs)


def main(params: Mapping[str, Any]) -> None:
    if params["list_functions"]:
        print_function_usage(FUNCTION_NAMES)
        return
    if not params["args"]:
        print(USAGE)
        return

    func_name, *pos_args = params["args"]

    if func_name not in FUNCTION_NAMES:
        raise NotImplementedError(
            f"Function provided as argument {func_name}"
            "is not supported or not yet been implemented"
        )

    func = getattr(core, func_name)
    kwargs: Dict[str, Union[str, int]] = dict()

    # Add to kwargs only the parameters plate,
    # pattern and index if they were passed
    for key in ("plate", "pattern", "index"):
        value = params.get(key)
        if value is not None:
            kwargs[key] = value

    res = call(func, *pos_args, **kwargs)
    # If func produces output, print it, else dont
    if res is not None:
        print(res)


if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(args)
