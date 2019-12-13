import asyncio
import os
import curses
from dataclasses import dataclass, replace
from typing import List

from intcode import IntcodeComputer, read_intlist

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

DISPLAY = True

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
    def __init__(self, program: List[int], window):
        self.window = window
        self.output = asyncio.Queue(maxsize=1)
        self.computer = IntcodeComputer(
            program, self.input_handler, self.output)

        self.score = 0
        self.grid = dict()
        self.ball = Point(-1, -1)
        self.paddle = Point(-1, -1)
        self.top_left = Point(0, 0)
        self.bottom_right = Point(0, 0)

    async def run(self):
        if self.window:
            curses.curs_set(False)
            self.window.erase()
            self.window.refresh()

        tasks = [
            asyncio.create_task(self.run_computer()),
            asyncio.create_task(self.output_handler())
        ]

        await asyncio.gather(*tasks)

    def print_grid(self):
        print('\033[H\033[J')

        for y in range(self.top_left.y, self.bottom_right.y + 1):
            for x in range(self.top_left.x, self.bottom_right.x + 1):
                if Point(x, y) in self.grid:
                    print(TILE_VALUES[self.grid[Point(x, y)]], end='')
            print()
        if self.score > 0:
            print(f'Current score: {self.score}')

    async def run_computer(self):
        await self.computer.execute()
        await self.output.put(99)
        await self.output.put(99)
        await self.output.put(99)

    async def output_handler(self):
        while True:
            x = await self.output.get()
            y = await self.output.get()
            value = await self.output.get()

            if (x == 99) and (y == 99) and (value == 99):
                break
            elif (x == -1) and (y == 0):
                self.score = value
                if self.window: self.window.addstr(0, 0, f'Score: {value:<8}', curses.A_REVERSE)
            else:
                self.grid[Point(x, y)] = value

                if self.window:
                    self.window.addch(y, x, TILE_VALUES[value])

                if value == TILE_BALL:
                    self.ball = Point(x, y)
                    if self.window: self.window.refresh()
                elif value == TILE_PADDLE:
                    self.paddle = Point(x, y)
                    if self.window: self.window.refresh()

                if x < self.top_left.x:
                    self.top_left = replace(self.top_left, x=x)
                if x > self.bottom_right.x:
                    self.bottom_right = replace(self.bottom_right, x=x)
                if y < self.top_left.y:
                    self.top_left = replace(self.top_left, y=y)
                if y > self.bottom_right.y:
                    self.bottom_right = replace(self.bottom_right, y=y)

            for _ in range(3):
                self.output.task_done()

    async def input_handler(self):
        await self.output.join()
        return self.calculate_input()

    def calculate_input(self) -> int:
        ball_x = self.ball.x
        paddle_x = self.paddle.x

        if ball_x < paddle_x:
            joystick_position = -1
        elif ball_x > paddle_x:
            joystick_position = 1
        else:
            joystick_position = 0

        return joystick_position


async def part1():
    game = GameComputer(read_intlist(input_file))
    await game.run()
    game.print_grid()

    block_tiles = sum(value == TILE_BLOCK for value in game.grid.values())
    print(f'Part 1: total {block_tiles} block tiles')


async def part2(window):
    program = read_intlist(input_file)
    program[0] = 2  # update number of coins
    game = GameComputer(program, window)
    await game.run()

    if window:
        window.getkey()
    else:
        print(f'Part 2: end score {game.score}')


def main(window):
    asyncio.run(part2(window))


if DISPLAY:
    curses.wrapper(main)
else:
    main()
