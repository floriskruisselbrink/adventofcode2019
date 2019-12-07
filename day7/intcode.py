from typing import List


def read_intlist(input_file: str) -> List[int]:
    with open(input_file) as input:
        line = input.readline()
        return [int(s) for s in line.split(',')]


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

    def set_instruction_pointer(self, instruction_pointer: int):
        self._instruction_pointer = instruction_pointer

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

    def next_instruction(self, instruction_pointer: int) -> int:
        return instruction_pointer + self.size()

    def execute(self, state: State, input: List[int]) -> int:
        next_ip = self.next_instruction(state._instruction_pointer)
        state.set_instruction_pointer(next_ip)


class AddInstruction(Instruction):
    def size(self) -> int: return 4

    def execute(self, state, input: List[int]):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = a + b

        state.write_parameter(2, result)
        super().execute(state, input)


class MultiplyInstruction(Instruction):
    def size(self) -> int: return 4

    def execute(self, state, input: List[int]):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = a * b

        state.write_parameter(2, result)
        super().execute(state, input)


class InputInstruction(Instruction):
    def size(self) -> int: return 2

    def execute(self, state, input: List[int]):
        value = input.pop(0)
        state.write_parameter(0, value)
        super().execute(state, input)


class OutputInstruction(Instruction):
    def size(self) -> int: return 2

    def execute(self, state, input: List[int]) -> int:
        output = state.read_parameter(0)
        super().execute(state, input)
        return output


class JumpIfTrueInstruction(Instruction):
    def size(self) -> int: return 3

    def execute(self, state, input):
        value = state.read_parameter(0)
        address = state.read_parameter(1)

        if (value != 0):
            state.set_instruction_pointer(address)
        else:
            super().execute(state, input)


class JumpIfFalseInstruction(Instruction):
    def size(self) -> int: return 3

    def execute(self, state, input):
        value = state.read_parameter(0)
        address = state.read_parameter(1)

        if (value == 0):
            state.set_instruction_pointer(address)
        else:
            super().execute(state, input)


class LessThanInstruction(Instruction):
    def size(self) -> int: return 4

    def execute(self, state, input):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = 1 if (a < b) else 0
        state.write_parameter(2, result)
        super().execute(state, input)


class EqualsInstruction(Instruction):
    def size(self) -> int: return 4

    def execute(self, state, input):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = 1 if (a == b) else 0
        state.write_parameter(2, result)
        super().execute(state, input)


class HaltInstruction(Instruction):
    # TODO: betere manier verzinnen om programma te beeindigen
    def size(self) -> int: return -9000


INSTRUCTION_MAP = {
    1: AddInstruction(),
    2: MultiplyInstruction(),
    3: InputInstruction(),
    4: OutputInstruction(),
    5: JumpIfTrueInstruction(),
    6: JumpIfFalseInstruction(),
    7: LessThanInstruction(),
    8: EqualsInstruction(),
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
        return instruction.execute(self._state, input)
