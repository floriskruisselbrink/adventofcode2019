import logging
from asyncio import Queue
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
    def __init__(self, program: List[int], input_queue: Queue, output_queue: Queue):
        self._memory = program.copy()
        self._input = input_queue
        self._output = output_queue
        self._instruction_pointer = 0

    def set_instruction_pointer(self, instruction_pointer: int):
        self._instruction_pointer = instruction_pointer

    def opcode(self) -> Opcode:
        if (self._instruction_pointer < 0):
            return None
        return Opcode(self._read(self._instruction_pointer))

    async def read_input(self) -> int:
        return await self._input.get()

    async def write_output(self, value: int):
        await self._output.put(value)

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

    async def execute(self, state: State):
        next_ip = self.next_instruction(state._instruction_pointer)
        state.set_instruction_pointer(next_ip)


class AddInstruction(Instruction):
    def size(self) -> int: return 4

    async def execute(self, state):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = a + b

        state.write_parameter(2, result)
        await super().execute(state)


class MultiplyInstruction(Instruction):
    def size(self) -> int: return 4

    async def execute(self, state):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = a * b

        state.write_parameter(2, result)
        await super().execute(state)


class InputInstruction(Instruction):
    def size(self) -> int: return 2

    async def execute(self, state):
        value = await state.read_input()
        logging.debug('Input %d', value)
        state.write_parameter(0, value)
        await super().execute(state)


class OutputInstruction(Instruction):
    def size(self) -> int: return 2

    async def execute(self, state):
        output = state.read_parameter(0)
        await state.write_output(output)
        logging.debug('Output %d', output)
        await super().execute(state)


class JumpIfTrueInstruction(Instruction):
    def size(self) -> int: return 3

    async def execute(self, state):
        value = state.read_parameter(0)
        address = state.read_parameter(1)

        if (value != 0):
            state.set_instruction_pointer(address)
        else:
            await super().execute(state)


class JumpIfFalseInstruction(Instruction):
    def size(self) -> int: return 3

    async def execute(self, state):
        value = state.read_parameter(0)
        address = state.read_parameter(1)

        if (value == 0):
            state.set_instruction_pointer(address)
        else:
            await super().execute(state)


class LessThanInstruction(Instruction):
    def size(self) -> int: return 4

    async def execute(self, state):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = 1 if (a < b) else 0
        state.write_parameter(2, result)
        await super().execute(state)


class EqualsInstruction(Instruction):
    def size(self) -> int: return 4

    async def execute(self, state):
        a = state.read_parameter(0)
        b = state.read_parameter(1)
        result = 1 if (a == b) else 0
        state.write_parameter(2, result)
        await super().execute(state)


class HaltInstruction(Instruction):
    # TODO: betere manier verzinnen om programma te beeindigen
    def size(self) -> int: return -9000

    async def execute(self, state):
        # TODO: cancel asyncio task
        await super().execute(state)


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
    def __init__(self, program: List[int], input_queue: Queue, output_queue: Queue):
        self._state = State(program, input_queue, output_queue)

    async def execute(self):
        current_opcode = self._state.opcode()
        while current_opcode is not None:
            instruction = INSTRUCTION_MAP[current_opcode.opcode]
            await instruction.execute(self._state)
            current_opcode = self._state.opcode()
