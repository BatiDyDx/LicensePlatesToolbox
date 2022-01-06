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

In general, every pattern can be shortened following the same pattern.

Some standard patterns are already given, and can be accessed through a
dictionary:

```python
# Spain's pattern
STD_PATTERNS["ES"] # "DDDDCCC"

# Denmark's pattern
STD_PATTERNS["DK"] # "CCDDDDD"
```

`STD_PATTERNS.keys()` will show all the patterns provided.

The keys to the dictionary are given by the ISO 3166-1 code for countries,
with some exceptions, like when a number is appended to it, indicating
that the country supports more than one pattern, or when a country is
subdivided. For the latter, the ISO 3166-2 standard is used.

The next code snippet illustrates the idea with an example:
```python
# Argentina's old pattern
STD_PATTERNS["AR-1"] # "CCCDDD"

# Argentina's new pattern
STD_PATTERNS["AR-2"] # "CCDDDCC"

# California pattern
STD_PATTERNS["US-CA"] # "DCCCDDD"
```

One can also look up for the ISO code of a country through
the ISO_3166 dictionary, in case of not knowing the corresponding
code assigned to the country. The key, if present, will be the name
of the country uppercased, and the value can match with three posibilites:

- A string corresponding to the ISO 3166-1 code to the country
- A list corresponding to multiple codes used
- A dictionary, whose keys are subdivions of the proper country, and
the values being the ISO 3166-2 code to the state/subdivision of the country

Following with the examples from above:
```python
# Codes associated to Argentina
ISO_3166["ARGENTINA"] # ["AR-1", "AR-2"]

# Codes associated to California
ISO_3166["USA"]["CALIFORNIA"] # "US-CA"
```

So one does not encounter the necessity to know the ISO 3166 codes.

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
