import asyncio
import logging
from typing import List

from intcode import IntcodeComputer
from utils import read_intlist


def test1():
    program = [3, 0, 4, 0, 99]
    input = [42]
    computer = IntcodeComputer(program)
    output = computer.execute(input)
    print(output)


def test2():
    program = [1002, 4, 3, 4, 33]
    input = []
    computer = IntcodeComputer(program)
    output = computer.execute(input)
    print(output)


async def execute_program(input: List[int]) -> List[int]:
    program = read_intlist('day5.txt')
    input_queue = asyncio.Queue()
    output_queue = asyncio.Queue()
    computer = IntcodeComputer(program, input_queue, output_queue)

    for i in input:
        input_queue.put_nowait(i)
    await computer.execute()

    output = []
    while not output_queue.empty():
        output.append(output_queue.get_nowait())
    return output


async def part1():
    input = [1]
    output = await execute_program(input)
    print("Part 1: {}".format(output))


async def part2():
    input = [5]
    output = await execute_program(input)
    print("Part 2: {}".format(output))

asyncio.run(part1())
asyncio.run(part2())
