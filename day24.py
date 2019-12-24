from __future__ import annotations

from typing import List

from utils import read_input_by_line


class Grid:
    def __init__(self, value: int):
        self.value = value

    def print(self):
        for i in range(25):
            print('#' if self.value & (1 << i) else '.', end='')
            if (i+1) % 5 == 0:
                print()

    def progress(self):
        new_value = 0
        for i in range(25):
            adjacent_bugs = sum(self.neighbours(i))

            if self.value & (1 << i):
                if adjacent_bugs == 1:
                    new_value += 1 << i
            else:
                if (adjacent_bugs == 1) or (adjacent_bugs == 2):
                    new_value += 1 << i

        self.value = new_value

    def get_field(self, i: int) -> bool:
        return bool(self.value & (1 << i))

    def neighbours(self, i: int) -> List[bool]:
        if i > 0 and (i % 5 != 0):
            yield self.get_field(i-1)
        if i > 4:
            yield self.get_field(i-5)
        if i < 24 and (i % 5 != 4):
            yield self.get_field(i+1)
        if i < 20:
            yield self.get_field(i+5)


NEIGHBOUR_DICT = {
    0: ((-1, 7), (-1, 11), (0, 1), (0, 5)),
    1: ((-1, 7), (0, 0), (0, 2), (0, 6)),
    2: ((-1, 7), (0, 1), (0, 3), (0, 7)),
    3: ((-1, 7), (0, 2), (0, 4), (0, 8)),
    4: ((-1, 7), (0, 3), (-1, 13), (0, 9)),
    5: ((0, 0), (-1, 11), (0, 6), (0, 10)),
    6: ((0, 1), (0, 5), (0, 7), (0, 11)),
    7: ((0, 2), (0, 6), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)),
    8: ((0, 3), (0, 7), (0, 9), (0, 13)),
    9: ((0, 4), (0, 8), (-1, 13), (0, 14)),
    10: ((0, 5), (-1, 11), (0, 11), (0, 15)),
    11: ((0, 6), (0, 10), (1, 0), (1, 5), (1, 10), (1, 15), (1, 20), (0, 16)),
    12: (),
    13: ((0, 8), (1, 4), (1, 9), (1, 14), (1, 19), (1, 24), (0, 14), (0, 18)),
    14: ((0, 9), (0, 13), (-1, 13), (0, 19)),
    15: ((0, 10), (-1, 11), (0, 16), (0, 20)),
    16: ((0, 11), (0, 15), (0, 17), (0, 21)),
    17: ((1, 20), (1, 21), (1, 22), (1, 23), (1, 24), (0, 16), (0, 18), (0, 22)),
    18: ((0, 13), (0, 17), (0, 19), (0, 23)),
    19: ((0, 14), (0, 18), (-1, 13), (0, 24)),
    20: ((0, 15), (-1, 11), (0, 21), (-1, 17)),
    21: ((0, 16), (0, 20), (0, 22), (-1, 17)),
    22: ((0, 17), (0, 21), (0, 23), (-1, 17)),
    23: ((0, 18), (0, 22), (0, 24), (-1, 17)),
    24: ((0, 19), (0, 23), (-1, 13), (-1, 17))
}


class GridLayer:
    def __init__(self, value: int, outer=None, inner=None):
        self.value = value
        self.new_value = None
        self.outer = outer
        self.inner = inner

        if inner:
            inner.outer = self
        if outer:
            outer.inner = self

    def count_bugs(self) -> int:
        return bin(self.value).count('1')

    def progress(self):
        self.new_value = 0
        for i in range(25):
            # skip center tile, it is only used for recursion
            if i == 12:
                continue

            adjacent_bugs = sum(self.neighbours(i))

            if self.get_field(i):
                # A bug dies unless there is exactly one bug adjacent to it.
                if adjacent_bugs == 1:
                    self.new_value += 1 << i
            else:
                # An empty space becomes invested with a bug if exactly one or two bugs are adjacent to it.
                if (adjacent_bugs == 1) or (adjacent_bugs == 2):
                    self.new_value += 1 << i

    def store_progress(self):
        self.value = self.new_value
        self.new_value = None

    def get_field(self, i: int) -> bool:
        assert i >= 0 and i < 25 and i != 12
        return bool(self.value & (1 << i))

    def neighbours(self, i: int) -> List[bool]:
        for layer, n in NEIGHBOUR_DICT[i]:
            if layer == 0:
                yield self.get_field(n)
            elif layer == 1:
                if self.inner:
                    yield self.inner.get_field(n)
                else:
                    yield False
            elif layer == -1:
                if self.outer:
                    yield self.outer.get_field(n)
                else:
                    yield False

    def print(self):
        for i in range(25):
            if i==12:
                print('?', end='')
            else:
                print('#' if self.value & (1 << i) else '.', end='')
            if (i+1) % 5 == 0:
                print()


class RecursiveGrid:
    def __init__(self, start_layer: GridLayer):
        self.layers = [start_layer]

    def count_bugs(self) -> int:
        return sum(layer.count_bugs() for layer in self.layers)

    def progress(self):
        outer_layer = GridLayer(0, inner=self.layers[0])
        inner_layer = GridLayer(0, outer=self.layers[-1])
        self.layers.insert(0, outer_layer)
        self.layers.append(inner_layer)

        for layer in self.layers:
            layer.progress()

        for layer in self.layers:
            layer.store_progress()

        if outer_layer.value == 0:
            self.layers.pop(0)
            self.layers[0].outer = None

        if inner_layer.value == 0:
            self.layers.pop(-1)
            self.layers[-1].inner = None

    def print(self):
        for i, layer in enumerate(self.layers):
            print(f'Layer {i}:')
            layer.print()


def parse_input(input: List[str]) -> int:
    result = 0
    for i, char in enumerate(''.join(input)):
        if char == '#':
            result += 1 << i

    return result


def part1(input: List[str]):
    grid = Grid(parse_input(input))
    seen_layouts = set()
    while not grid.value in seen_layouts:
        seen_layouts.add(grid.value)
        grid.progress()

    print(f'Part 1: first layout that appears twice: {grid.value}')


def part2(input: List[str], minutes: int):
    start_layer = GridLayer(parse_input(input))
    grid = RecursiveGrid(start_layer)
    
    for i in range(minutes):
        grid.progress()

    print(
        f'Part 2: number of bugs after {minutes} minutes: {grid.count_bugs()}')


test_input = [
    '....#',
    '#..#.',
    '#..##',
    '..#..',
    '#....']

puzzle_input = [
    '##.#.',
    '#.###',
    '##...',
    '...#.',
    '#.##.'
]

part1(puzzle_input)
part2(puzzle_input, 200)
