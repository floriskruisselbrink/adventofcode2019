from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import List


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: Point) -> Point:
        return Point(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Velocity(Point):
    def __init__(self):
        super().__init__(0, 0, 0)


@dataclass
class Moon:
    pos: Point
    velocity: Velocity = field(default_factory=Velocity)

    def total_energy(self) -> int:
        return self.pos.energy() * self.velocity.energy()


class MoonSystem:
    def __init__(self, moons: List[Moon]):
        self.moons = moons

    def total_energy(self) -> int:
        return sum(m.total_energy() for m in self.moons)

    def execute_timestep(self):
        for a, b in combinations(self.moons, 2):
            self.apply_gravity(a, b)
        for m in self.moons:
            m.pos += m.velocity

    def apply_gravity(self, a: Moon, b: Moon):
        if (a.pos.x != b.pos.x):
            a.velocity.x += 1 if a.pos.x < b.pos.x else -1
            b.velocity.x += 1 if b.pos.x < a.pos.x else -1
        if (a.pos.y != b.pos.y):
            a.velocity.y += 1 if a.pos.y < b.pos.y else -1
            b.velocity.y += 1 if b.pos.y < a.pos.y else -1
        if (a.pos.z != b.pos.z):
            a.velocity.z += 1 if a.pos.z < b.pos.z else -1
            b.velocity.z += 1 if b.pos.z < a.pos.z else -1


def part1(moons: List[Moon], steps: int, verbose: bool = False):
    system = MoonSystem(moons)
    for time_step in range(steps):
        system.execute_timestep()

    total_energy = system.total_energy()
    print(f'Part 1: total energy {total_energy}')


def part2(moons: List[Moon]):
    pass


sample1 = [
    Moon(Point(-1, 0, 2)),
    Moon(Point(2, -10, -7)),
    Moon(Point(4, -8, 8)),
    Moon(Point(3, 5, -1))
]
sample2 = [
    Moon(Point(-8, -10, 0)),
    Moon(Point(5, 5, 10)),
    Moon(Point(2, -7, 3)),
    Moon(Point(9, -8, -3))
]
puzzle = [
    Moon(Point(-10, -13, 7)),
    Moon(Point(1, 2, 1)),
    Moon(Point(-15, -3, 13)),
    Moon(Point(3, 7, -4))
]

# part1(sample1, 10, verbose=True) # 179
# part1(sample2, 100, verbose=True) # 1940
part1(puzzle, 1000)
