import logging
import os
from typing import List
from intcode import IntcodeComputer, read_intlist

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


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



def execute_program(input: List[int]) -> List[int]:
    program = read_intlist(input_file)
    computer = IntcodeComputer(program)
    return computer.execute(input)

def part1():
    input = [1]
    output = execute_program(input)
    print("Part 1: {}".format(output))

def part2():
    input = [5]
    output = execute_program(input)
    print("Part 2: {}".format(output))

part1()
part2()
