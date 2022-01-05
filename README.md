# License Plate Toolbox

![Tests](https://github.com/BatiDyDx/LicensePlatesToolbox/actions/workflows/tests.yml/badge.svg)

This project provides a simple way to operate with license plates
and its patterns.

## Installation

To install the module, just run on the command line:

```console
$ pip install plates
```

## Module usage

For example, to get the number of possible plates with a given pattern:
```python
from plates import *
combinations("CCCDDD") # 17576000
```

In the example above, the pattern given corresponds to 3 characters and 3
digits. ABC123 is a plate that matches with this pattern, then:
```python
matches_pattern("CCCDDD", "ABC123") # True
```

The above pattern can be shortened as `"3C3D"`, meaning 3 chars and 3 digits.

Some standard patterns are already given, and can be accessed through 
dictionary:

```python
# Argentina's old pattern
STD_PATTERNS["AR-1"] # "CCCDDD"

# Argentina's new pattern
STD_PATTERNS["AR-2"] # "CCDDDCC"

# California pattern
STD_PATTERNS["US-CA"] # "DCCCDDD"
```

`STD_PATTERNS.keys()` will show all the patterns provided.

## Command line usage

The tools provided can be used directly through the command line, invoking the
plates module and passing the function name with it's proper positional or
keyword arguments. Here's an example:

```console
$ python -m plates get_pattern AB5472D
```

will produce `CCDDDDC` as the result.

To get a list of all the available functions for the command line, call the
module with the `-lf` or `--list-functions` flag, and it will print a list
of supported functions with its arguments and respective types.

For help using the module via the command line, pass the `-h` or `--help` flag.

Some basics examples are:
```console
$ python -m plates max_plate --pattern CCDDDC
```
```console
$ python -m plates get_plate -p CCDDDC -i 168700
```
```console
$ python -m plates get_plate_index -pl GA155RT
```
