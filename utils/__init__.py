from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, List


def reverse(string):
    string = "".join(reversed(string))
    return string

def flatten(l: List[Any]):
    """ Flatten a (possibly recursively) nested list to one flat list """
    if l == []:
        return l
    if isinstance(l[0], list):
        return flatten(l[0]) + flatten(l[1:])
    return l[:1] + flatten(l[1:])


def read_line(input_file: str) -> str:
    with open(_file_path(input_file)) as input:
        return input.readline().rstrip()


def read_input_by_line(input_file: str) -> List[str]:
    with open(_file_path(input_file)) as input:
        return input.read().splitlines()


def read_intlist(input_file: str) -> List[int]:
    with open(_file_path(input_file)) as input:
        line = input.readline()
        return [int(s) for s in line.split(',')]


def _file_path(input_file: str) -> str:
    return os.path.join(os.path.dirname(__file__), '../input', input_file)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self):
        return f'({self.x},{self.y})'

    def neighbours(self, filter: Callable[[Point], bool] = lambda _: True) -> List[Point]:
        """ Find all neighbours to this point. """
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        result = []
        for (x, y) in directions:
            neighbour = Point(self.x + x, self.y + y)
            if filter(neighbour):
                result.append(neighbour)
        return result
