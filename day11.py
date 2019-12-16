from __future__ import annotations

import asyncio
from dataclasses import dataclass, field, replace
from typing import List

from intcode import IntcodeComputer
from utils import read_intlist

WHITE = 1
BLACK = 0

MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3

TURN_LEFT = 0
TURN_RIGHT = 1


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __repr__(self): return f'({self.x},{self.y})'

    def point_in_direction(self, direction: int) -> Point:
        if direction == MOVE_UP:
            return Point(self.x, self.y - 1)
        elif direction == MOVE_RIGHT:
            return Point(self.x + 1, self.y)
        elif direction == MOVE_DOWN:
            return Point(self.x, self.y + 1)
        elif direction == MOVE_LEFT:
            return Point(self.x - 1, self.y)


class PaintingRobot:
    def __init__(self, program: List[int], starting_color: int):
        self.input = asyncio.Queue()
        self.output = asyncio.Queue()
        self.computer = IntcodeComputer(program, self.input, self.output)
        self.position = Point(0, 0)
        self.direction = MOVE_UP
        self.is_running = False
        self.tiles_painted = 0

        self.top_left = Point(0, 0)
        self.bottom_right = Point(0, 0)
        self.grid = {}
        self.paint_current_tile(starting_color)

    async def execute(self):
        self.is_running = True

        tasks = [
            asyncio.create_task(self.run_computer()),
            asyncio.create_task(self.handle_inout())
        ]
        await asyncio.gather(*tasks)

    async def run_computer(self):
        await self.computer.execute()
        self.is_running = False

    async def handle_inout(self):
        while self.is_running:
            await self.input.put(self.get_current_tile())

            color = await self.output.get()
            self.paint_current_tile(color)

            turn = await self.output.get()
            self.move_in_direction(turn)

    def get_current_tile(self) -> int:
        if self.position in self.grid:
            return self.grid[self.position]
        else:
            return BLACK

    def paint_current_tile(self, color: int):
        if not self.position in self.grid:
            self.tiles_painted += 1

        self.grid[self.position] = color

    def move_in_direction(self, turn: int):
        if turn == TURN_LEFT:
            self.direction = (self.direction-1) % 4
        elif turn == TURN_RIGHT:
            self.direction = (self.direction+1) % 4

        self.position = self.position.point_in_direction(self.direction)

        if not self.position in self.grid:
            if (self.position.x < self.top_left.x):
                self.top_left = replace(self.top_left, x=self.position.x)
            if (self.position.y < self.top_left.y):
                self.top_left = replace(self.top_left, y=self.position.y)
            if (self.position.x > self.bottom_right.x):
                self.bottom_right = replace(
                    self.bottom_right, x=self.position.x)
            if (self.position.y > self.bottom_right.y):
                self.bottom_right = replace(
                    self.bottom_right, y=self.position.y)

    def print_grid(self):
        print(f'Top left: {self.top_left}, bottom right: {self.bottom_right}')

        # TODO fix off by one error
        for y in range(self.top_left.y, (self.bottom_right.y - self.top_left.y)+1):
            for x in range(self.top_left.x, (self.bottom_right.x - self.top_left.x)+1):
                if Point(x, y) == self.position:
                    color = '@'
                elif Point(x, y) in self.grid:
                    color = '#' if self.grid[Point(x, y)] == 1 else '.'
                else:
                    color = ' '
                print(color, end='')
            print()


def test1():
    robot = PaintingRobot([], BLACK)
    robot.paint_current_tile(WHITE)
    robot.move_in_direction(TURN_LEFT)
    robot.paint_current_tile(BLACK)
    robot.move_in_direction(TURN_LEFT)
    robot.paint_current_tile(WHITE)
    robot.move_in_direction(TURN_LEFT)
    robot.paint_current_tile(WHITE)
    robot.move_in_direction(TURN_LEFT)
    robot.paint_current_tile(BLACK)
    robot.move_in_direction(TURN_RIGHT)
    robot.paint_current_tile(WHITE)
    robot.move_in_direction(TURN_LEFT)
    robot.paint_current_tile(WHITE)
    robot.move_in_direction(TURN_LEFT)

    robot.print_grid()
    print(f'Test1: {robot.tiles_painted} tiles painted')


async def part1():
    program = read_intlist('day11.txt')
    robot = PaintingRobot(program, BLACK)
    await robot.execute()
    robot.print_grid()
    print(f'Part1: {robot.tiles_painted} tiles painted')


async def part2():
    program = read_intlist('day11.txt')
    robot = PaintingRobot(program, WHITE)
    await robot.execute()
    robot.print_grid()
    print(f'Part2: {robot.tiles_painted} tiles painted')

test1()
asyncio.run(part1())
asyncio.run(part2())
