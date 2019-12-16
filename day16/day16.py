import os
from itertools import cycle
from typing import Iterator

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

FFT_PATTERN = [0, 1, 0, -1]


def create_pattern(position: int) -> Iterator:
    return [i for i in FFT_PATTERN for _ in range(position)]


def fft(input_signal: str, phases: int) -> int:
    input_data = list(map(int, list(input_signal)))

    for phase in range(1, phases+1):
        output_signal = ''
        for i in range(len(input_data)):
            pattern = cycle(create_pattern(i+1))
            next(pattern) # skip first value exactly once

            output = 0
            for input in input_data:
                np = next(pattern)
                output += input * np
                #print(f'{input}*{np} + ', end='')
            #print(f'\b\b = {output}')
            output_signal += str(abs(output) % 10)
        
        #print(f'After phase {phase}: {output_signal}')
        input_data = list(map(int, list(output_signal)))

    return output_signal


def part1():
    with open(input_file) as input:
        input_signal = input.read().replace('\n', '')

    print(f'Part 1: {fft(input_signal, 100)}')


def tests():
    print(f'12345678 becomes {fft("12345678", 4)}')
    print(f'80871224585914546619083218645595 becomes {fft("80871224585914546619083218645595", 100)} ')
    print(f'19617804207202209144916044189917 becomes {fft("19617804207202209144916044189917", 100)}')


# tests()
part1()
