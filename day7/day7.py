import asyncio
import itertools
import logging
import os
import string
from asyncio import Queue
from typing import List

from intcode import IntcodeComputer, read_intlist

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


async def amplifier_worker(name: str, program: List[int], input: Queue, output: Queue):
    amplifier = IntcodeComputer(program, input, output)
    logging.debug('%s created', name)
    await amplifier.execute()
    logging.debug('%s finished', name)


async def try_amplifier(program: List[int], phases: List[int]):
    tasks = []
    first_queue = Queue()

    input_queue = first_queue
    for i, phase in enumerate(phases):
        input_queue.put_nowait(phase)

        if (i == (len(phases) - 1)):
            output_queue = first_queue
        else:
            output_queue = Queue()

        name = string.ascii_uppercase[i]
        task = asyncio.create_task(amplifier_worker(
            name, program, input_queue, output_queue))
        tasks.append(task)

        input_queue = output_queue

    # Initialize first amplifier
    first_queue.put_nowait(0)

    await asyncio.gather(*tasks)
    return first_queue.get_nowait()


async def test1():
    program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    phase_sequences = itertools.permutations([0, 1, 2, 3, 4])

    max_thrust = -1
    for phases in phase_sequences:
        thrust = await try_amplifier(program, phases)
        max_thrust = max(thrust, max_thrust)
    print(f'Test1: {max_thrust}')


async def part1():
    program = read_intlist(input_file)
    phase_sequences = itertools.permutations([0, 1, 2, 3, 4])

    max_thrust = -1
    for phases in phase_sequences:
        thrust = await try_amplifier(program, phases)
        max_thrust = max(thrust, max_thrust)
    print(f'Part 1: {max_thrust}')


asyncio.run(part1())
