import itertools
import os
from typing import List

from intcode import IntcodeComputer, read_intlist

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


class AmplifierSetup:
    def __init__(self, program: List[int]):
        self.program = program

    def execute(self, phase_sequence: List[int]) -> int:
        amp_input = 0
        for phase in phase_sequence:
            computer = IntcodeComputer(self.program)
            output = computer.execute([phase, amp_input])
            #print("Phase {}, input {}, output {}".format(phase, amp_input, output))
            amp_input = output.pop()

        return amp_input

def find_max_thrust(program: List[int], phases: List[int]) -> int:
    phase_sequences = itertools.permutations(phases)

    max_thrust = -1
    for phase_sequence in phase_sequences:
        amplifier = AmplifierSetup(program)
        thrust = amplifier.execute(phase_sequence)
        #print("{}: {}".format(phase_sequence, thrust))
        max_thrust = max(thrust, max_thrust)

    return max_thrust

def part1():
    program = read_intlist(input_file)
    max_thrust = find_max_thrust(program, [0, 1, 2, 3, 4])
    print("Part 1: {}".format(max_thrust))

def test1():
    program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    max_thrust = find_max_thrust(program)

    print("Max thrust: {}".format(max_thrust))


part1()
