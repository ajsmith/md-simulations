#!/usr/bin/env python

from math import ceil
import sys


def max_atom_coord(line):
    fields = line.split()
    coords = [abs(float(s)) for s in fields[6:9]]
    return max(coords)


def main():
    (_, filepath) = sys.argv
    max_coord = 0
    with open(filepath) as f:
        for (lineno, line) in enumerate(f.readlines()):
            if line.startswith('ATOM'):
                coord = max_atom_coord(line)
                if coord > max_coord:
                    max_coord = coord
        cell_size = 2 * (ceil(max_coord) + 10)
        print(f'L/2 = {max_coord}')
        print(f'Unit Cell Size = {cell_size}')


if __name__ == '__main__':
    main()
