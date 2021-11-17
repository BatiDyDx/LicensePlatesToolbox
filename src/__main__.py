import argparse
import json
import pathlib
import lic_plates as lp

PATH = pathlib.Path(__file__)

with open(PATH.parent / "prog_info.json") as f:
    json_file = json.loads(f.read())
    
    programme_info = json_file["License Plates"]["Programme Info"]
    prog_usage = programme_info["Programme Usage"]
    prog_description = programme_info["Programme Description"]
    prog_epilog = programme_info["Programme Epilog"]

    help_str = json_file["License Plates"]["Function Help Strings"]


parser = argparse.ArgumentParser(
    prog = "License Plates",
    usage = prog_usage,
    description= prog_description,
    add_help = True,
    epilog=prog_epilog,
)


parser.add_argument(
    dest="command",
)

parser.add_argument(
    dest="args",
)

parser.add_argument(
    "-v", "--version",
)


def main() -> None:
    #user_input = parser.parse_args()
    #args = vars(user_input)
    
    # Test Warnings
    print(lp.get_plate(lp.STD_PATTERNS["AR1"], lp.combinations(lp.STD_PATTERNS["AR1"]) + 1))

if __name__ == "__main__":
    main()