from typing import List

from utils import read_input_by_line


class Grid:
    def __init__(self, input: str):
        self.value = 0
        for i, char in enumerate(input):
            if char == '#':
                self.value += 1 << i

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

    def neighbours(self, i: int) -> List[bool]:
        if i > 0 and (i % 5 != 0):
            yield bool(self.value & (1 << (i-1)))
        if i > 4:
            yield bool(self.value & (1 << (i-5)))
        if i < 24 and (i % 5 != 4):
            yield bool(self.value & (1 << (i+1)))
        if i < 20:
            yield bool(self.value & (1 << (i+5)))


def part1(input: List[str]):
    grid = Grid(''.join(input))
    seen_layouts = set()
    while not grid.value in seen_layouts:
        seen_layouts.add(grid.value)
        grid.progress()

    print(f'First layout that appears twice: {grid.value}')


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
