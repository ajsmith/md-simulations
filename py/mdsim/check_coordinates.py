#!/usr/bin/env python
from functools import partial
import sys


def validate_atom_line(max_dist, line):
    fields = line.split()
    coords = map(float, fields[6:9])
    return all(abs(v) <= max_dist for v in coords)


def get_atom_validator(max_dist):
    return partial(validate_atom_line, max_dist)


def main():
    (_, filename, max_dist) = sys.argv
    max_dist = float(max_dist)
    is_valid_atom = get_atom_validator(max_dist)
    with open(filename) as f:
        for (lineno, line) in enumerate(f.readlines()):
            if line.startswith('ATOM') and not is_valid_atom(line):
                print('ERROR: Invalid atom at line ', lineno + 1)
                print(line.rstrip())
                sys.exit(1)
        print('All good!')


if __name__ == '__main__':
    main()
