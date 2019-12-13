import asyncio
import os

from typing import List
from dataclasses import dataclass, replace
from intcode import IntcodeComputer, read_intlist

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4

TILE_VALUES = [' ', u'\u2588', '#', '_', 'o']

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class GameComputer:
    def __init__(self, program: List[int]):
        self.input = asyncio.Queue()
        self.output = asyncio.Queue()
        self.computer = IntcodeComputer(program, self.input, self.output)
        
        self.grid = dict()
        self.top_left = Point(0, 0)
        self.bottom_right = Point(0, 0)

    async def run(self):
        tasks = [
            asyncio.create_task(self.run_computer()),
            asyncio.create_task(self.io_handler())
        ]

        await asyncio.gather(*tasks)

    def print_grid(self):
        for y in range(self.top_left.y, self.bottom_right.y + 1):
            for x in range(self.top_left.x, self.bottom_right.x + 1):
                if Point(x, y) in self.grid:
                    print(TILE_VALUES[self.grid[Point(x, y)]], end='')
            print()

    async def run_computer(self):
        await self.computer.execute()
        await self.output.put(99)

    async def io_handler(self):
        while True:
            x = await self.output.get()
            if (x == 99): break

            y = await self.output.get()
            value = await self.output.get()

            self.grid[Point(x, y)] = value

            if x < self.top_left.x:
                self.top_left = replace(self.top_left, x = x)
            if x > self.bottom_right.x:
                self.bottom_right = replace(self.bottom_right, x = x)
            if y < self.top_left.y:
                self.top_left = replace(self.top_left, y = y)
            if y > self.bottom_right.y:
                self.bottom_right = replace(self.bottom_right, y = y)
            

async def part1():
    game = GameComputer(read_intlist(input_file))
    await game.run()
    game.print_grid()

    block_tiles = sum(value == TILE_BLOCK for value in game.grid.values())
    print(f'Part 1: total {block_tiles} block tiles')

asyncio.run(part1())