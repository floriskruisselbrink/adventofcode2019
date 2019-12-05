import os
from typing import List

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

def read_intlist(input_file: str) -> List[int]:
    with open(input_file) as input:
        line = input.readline()
        return [int(s) for s in line.split(',')]

def add(environment: List[int], a: int, b: int, c: int):
    result = environment[a] + environment[b]
    environment[c] = result

def multiply(environment: List[int], a: int, b: int, c: int):
    result = environment[a] * environment[b]
    environment[c] = result

def execute_opcode(environment: List[int], instruction_pointer: int) -> int:
    opcode = environment[instruction_pointer]
    if opcode == 99:
        return -1

    a = environment[instruction_pointer+1]
    b = environment[instruction_pointer+2]
    c = environment[instruction_pointer+3]
    if opcode == 1:
        add(environment, a, b, c)
        return instruction_pointer + 4
    elif opcode == 2:
        multiply(environment, a, b, c)
        return instruction_pointer + 4

def execute_program(program: List[int], noun: int, verb: int) -> int:
    environment = program.copy()
    environment[1] = noun
    environment[2] = verb

    instruction_pointer = 0
    while (instruction_pointer >= 0):
        instruction_pointer = execute_opcode(environment, instruction_pointer)

    return environment[0]

def part1(input_file: str):
    program = read_intlist(input_file)
    result = execute_program(program, 12, 2)

    print('Part 1: {}'.format(result))

def part2(input_file: str):
    program = read_intlist(input_file)

    expected_output = 19690720

    for noun in range(99):
        for verb in range(99):
            output = execute_program(program, noun, verb)
            if output == expected_output:
                print('Part 2: {}'.format(100*noun+verb))
                return

part1(input_file)
part2(input_file)
