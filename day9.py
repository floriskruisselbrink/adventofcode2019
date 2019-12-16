import asyncio
from asyncio import Queue
from typing import List

from intcode import IntcodeComputer
from utils import read_intlist


async def run_program(program: List[int], input_signal: int):
    input = Queue()
    output = Queue()
    computer = IntcodeComputer(program, input, output)

    input.put_nowait(input_signal)

    await computer.execute()

    while not output.empty():
        print(output.get_nowait())


async def part1():
    program = read_intlist('day9.txt')
    print('Part 1:')
    await run_program(program, 1)


async def part2():
    program = read_intlist('day9.txt')
    print('Part 2:')
    await run_program(program, 2)


async def test1():
    program = [109, 1, 204, -1, 1001, 100, 1,
               100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    print('Test 1')
    await run_program(program, 1)


async def test2():
    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    print('Test 2')
    await run_program(program, 1)


async def test3():
    program = [104, 1125899906842624, 99]
    print('Test 3')
    await run_program(program, 1)


asyncio.run(part1())
asyncio.run(part2())
