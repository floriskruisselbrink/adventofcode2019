import logging
import os
from typing import List

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

def reverse(string: str) -> str:
    string = "".join(reversed(string))
    return string

class Opcode:
    def __init__(self, instruction: int):
        self.opcode = instruction % 100
        self._parameter_mode = reverse(str(instruction // 100)) + '0000'

    def parameter_mode(self, parameter: int) -> int:
        """ mode 0 = position mode, mode 1 = immediate mode """
        return int(self._parameter_mode[parameter])


class State:
    def __init__(self, program: List[int]):
        self._memory = program.copy()
        self._instruction_pointer = 0

    def next_instruction(self, offset: int):
        self._instruction_pointer += offset

    def opcode(self) -> Opcode:
        if (self._instruction_pointer < 0):
            return None
        return Opcode(self._read(self._instruction_pointer))

    def read_parameter(self, index: int) -> int:
        """ first parameter has index 0 """
        opcode = self.opcode()
        parameter_mode = opcode.parameter_mode(index)
        if (parameter_mode == 0):
            address = self._read(self._instruction_pointer + index + 1)
            return self._read(address)
        else:
            return self._read(self._instruction_pointer + index + 1)

    def write_parameter(self, index: int, value: int):
        """ reads address from parameter index, writes value to that position """
        address = self._read(self._instruction_pointer + index + 1)
        self._write(address, value)

    def _read(self, address: int) -> int:
        return self._memory[address]

    def _write(self, address: int, value: int):
        self._memory[address] = value


class Instruction:
    def size(self) -> int:
        pass

    def execute(self, state: State, input: List[int]) -> int:
        pass


class AddInstruction(Instruction):
    def size(self) -> int: return 4

    def execute(self, state, input: List[int]):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = a + b

        state.write_parameter(2, result)


class MultiplyInstruction(Instruction):
    def size(self) -> int: return 4

    def execute(self, state, input: List[int]):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = a * b

        state.write_parameter(2, result)


class InputInstruction(Instruction):
    def size(self) -> int: return 2

    def execute(self, state, input: List[int]):
        value = input.pop()
        state.write_parameter(0, value)


class OutputInstruction(Instruction):
    def size(self) -> int: return 2

    def execute(self, state, input: List[int]) -> int:
        return state.read_parameter(0)


class HaltInstruction(Instruction):
    # TODO: betere manier verzinnen om programma te beeindigen
    def size(self) -> int: return -9000


INSTRUCTION_MAP = {
    1: AddInstruction(),
    2: MultiplyInstruction(),
    3: InputInstruction(),
    4: OutputInstruction(),
    99: HaltInstruction()
}


class IntcodeComputer:
    def __init__(self, program: List[int]):
        self._state = State(program)

    def execute(self, input: List[int]) -> List[int]:
        output = []

        while self._state.opcode() is not None:
            opcode_output = self._execute_opcode(self._state.opcode(), input)
            if opcode_output is not None:
                output.append(opcode_output)
        return output

    def _execute_opcode(self, opcode: Opcode, input: List[int]) -> int:
        instruction = INSTRUCTION_MAP[opcode.opcode]
        output = instruction.execute(self._state, input)
        self._state.next_instruction(instruction.size())
        return output


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

def read_intlist(input_file: str) -> List[int]:
    with open(input_file) as input:
        line = input.readline()
        return [int(s) for s in line.split(',')]

def part1():
    program = read_intlist(input_file)
    input = [1]
    computer = IntcodeComputer(program)
    output = computer.execute(input)
    print("Part 1: {}".format(output))

part1()