from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Tuple
from math import gcd
from functools import reduce
from copy import deepcopy

@dataclass
class Point:
    axes: List[int]

    def __init__(self, x, y, z):
        self.axes = [x, y, z]

    def __getitem__(self, key) -> int:
        return self.axes[key]

    def __setitem__(self, key: int, value: int):
        self.axes[key] = value

    def __repr__(self):
        return f'<x={self.axes[0]:3}, y={self.axes[1]:3}, z={self.axes[2]:3}>'


class Moon:
    def __init__(self, position: Point):
        self.initial_position = position
        self.initial_velocity = Point(0, 0, 0)

        self.position = deepcopy(self.initial_position)
        self.velocity = deepcopy(self.initial_velocity)

    def total_energy(self):
        potential = sum(abs(n) for n in self.position)
        kinetic = sum(abs(n) for n in self.velocity)
        return potential * kinetic

    def __repr__(self):
        return f'pos={self.position}, vel={self.velocity}'


class MoonSystem:
    def __init__(self, moons: List[Moon]):
        self.moons = moons.copy()

    def total_energy(self):
        return sum(m.total_energy() for m in self.moons)

    def time_step(self):
        for axis in range(3):
            self.time_step_axis(axis)

    def time_step_axis(self, axis: int):
        self.apply_gravity(axis)
        self.move_moons(axis)

    def apply_gravity(self, axis: int):
        for a, b in combinations(self.moons, 2):
            if (a.position[axis] < b.position[axis]):
                a.velocity[axis] += 1
                b.velocity[axis] -= 1
            elif (a.position[axis] > b.position[axis]):
                a.velocity[axis] -= 1
                b.velocity[axis] += 1

    def move_moons(self, axis: int):
        for m in self.moons:
            m.position[axis] += m.velocity[axis]

    def is_initial_state(self) -> bool:
        for m in self.moons:
            if m.position != m.initial_position:
                return False
            elif m.velocity != m.initial_velocity:
                return False
        return True


def lcm(a, b):
    return int(a * b / gcd(a, b))


def part1(moons: List[Moon], steps: int):
    system = MoonSystem(moons)
    for step in range(steps):
        #print(f'After {step} steps:')
        # for m in system.moons:
        #    print(m)

        system.time_step()

    print(f'Part 1: total energy {system.total_energy()}')


def part2(moons: List[Moon]):
    system = MoonSystem(moons)

    iterations = []

    for axis in range(3):
        iteration = 1
        system.time_step_axis(axis)
        while not system.is_initial_state():
            system.time_step_axis(axis)
            iteration += 1
        iterations.append(iteration)

    result = reduce(lcm, iterations)
    print(f'Part 2: {result}')


def sample1():
    return [
        Moon(Point(-1, 0, 2)),
        Moon(Point(2, -10, -7)),
        Moon(Point(4, -8, 8)),
        Moon(Point(3, 5, -1))
    ]


def sample2():
    return [
        Moon(Point(-8, -10, 0)),
        Moon(Point(5, 5, 10)),
        Moon(Point(2, -7, 3)),
        Moon(Point(9, -8, -3))
    ]


def puzzle():
    return [
        Moon(Point(-10, -13, 7)),
        Moon(Point(1, 2, 1)),
        Moon(Point(-15, -3, 13)),
        Moon(Point(3, 7, -4))
    ]


# part1(sample1, 10)  # 179
# part1(sample2, 100)  # 1940
part1(puzzle(), 1000)

# part2(sample1) # 2772
# part2(sample2) # 4686774924
part2(puzzle())
