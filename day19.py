import asyncio
from typing import List

from intcode import IntcodeComputer
from utils import Point



async def part1(grid_size: int):
    input = asyncio.Queue()
    output = asyncio.Queue()
    computer = IntcodeComputer('day19.txt', input, output)

    grid = [['?' for x in range(grid_size)] for y in range(grid_size)]
    affected_points = 0
    for x in range(grid_size):
        for y in range(grid_size):
            computer.reset()
            input.put_nowait(x)
            input.put_nowait(y)
            await computer.execute()
            result = output.get_nowait()

            if result == 1:
                affected_points += 1
                grid[y][x] = '#'
            else:
                grid[y][x] = '.'
    
    for line in grid:
        print(''.join(line))
    
    print(f'Part 1: {affected_points}')
    


asyncio.run(part1(50))