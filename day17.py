import asyncio
import curses
from typing import List, Set

from intcode import IntcodeComputer
from utils import Point


class Grid:
    def __init__(self,):
        self.grid = []

    def find_alignment(self) -> List[int]:
        return [p.x * p.y for p in self.find_intersections()]

    def find_intersections(self) -> Set[Point]:
        intersections = set()

        for y in range(1, len(self.grid)-2):
            for x in range(1, len(self.grid[0])-2):
                neighbours = self.all_neighbours(x, y)
                if all(n == '#' for n in neighbours):
                    intersections.add(Point(x, y))

        return intersections

    def all_neighbours(self, x: int, y: int) -> List[str]:
        return [
            self[y][x],
            self[y-1][x],
            self[y][x-1],
            self[y+1][x],
            self[y][x+1],
        ]

    def append(self, value: str):
        self.grid.append(list(value))

    def __getitem__(self, key) -> str:
        return "".join(self.grid[key])

    def __setitem__(self, key: int, value: str):
        self.grid[key] = list(value)


async def part1():
    input = asyncio.Queue()
    output = asyncio.Queue()
    computer = IntcodeComputer('day17.txt', input, output)
    await computer.execute()

    grid = Grid()
    line = ''
    while not output.empty():
        out = await output.get()
        if out != 10:
            line += chr(out)
        elif line != '':
            grid.append(line)
            line = ''

    alignments = grid.find_alignment()

    for line in grid:
        print(line)
    print(f'Part 1: {sum(alignments)}')

asyncio.run(part1())
