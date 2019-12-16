import os
from typing import List


def read_line(input_file: str) -> str:
    with open(_file_path(input_file)) as input:
        return input.readline().rstrip()


def read_input_by_line(input_file: str) -> List[str]:
    with open(_file_path(input_file)) as input:
        return input.read().splitlines()


def read_intlist(input_file: str) -> List[int]:
    with open(_file_path(input_file)) as input:
        line = input.readline()
        return [int(s) for s in line.split(',')]


def _file_path(input_file: str) -> str:
    return os.path.join(os.path.dirname(__file__), '../input', input_file)
