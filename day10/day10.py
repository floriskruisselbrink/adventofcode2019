import os
from dataclasses import dataclass
from math import atan2
from typing import List, Set, Tuple



@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self): return f'({self.x},{self.y})'


class AsteroidMap:
    def __init__(self, input: List[str]):
        self.asteroids = set()
        self.max_x = len(input[0]) - 1
        self.max_y = len(input)

        for y, line in enumerate(input):
            for x, column in enumerate(line):
                if column == '#':
                    self.asteroids.add(Point(x, y))
    
    def count_visible_asteroids(self, viewing_point: Point) -> int:
        other_asteroids = self.asteroids.copy()
        other_asteroids.remove(viewing_point)

        viewing_angles = set()
        for asteroid in other_asteroids:
            angle = atan2(asteroid.y - viewing_point.y, asteroid.x - viewing_point.x)
            viewing_angles.add(angle)

        return len(viewing_angles)

    def find_best_location_for_ims(self) -> Tuple[int, Point]:
        max_asteroid = None
        max_count = -1
        for asteroid in self.asteroids:
            count = self.count_visible_asteroids(asteroid)
            if count > max_count:
                max_count = count
                max_asteroid = asteroid

        return max_count, max_asteroid

def read_file(filename: str) -> List[str]:
    input_file = os.path.join(os.path.dirname(__file__), filename)
    with open(input_file) as input:
        lines = input.read().splitlines()
    return lines

def part1(filename: str) -> Tuple[int, Point]:
    map = AsteroidMap(read_file(filename))

    count, asteroid = map.find_best_location_for_ims()
    print(f'{filename}: {count} visible from {asteroid}')
    return count, asteroid

assert part1('dummy0.txt') == (8, Point(3, 4))
assert part1('dummy1.txt') == (33, Point(5, 8))
assert part1('dummy2.txt') == (35, Point(1, 2))
assert part1('dummy3.txt') == (41, Point(6, 3))
assert part1('dummy4.txt') == (210, Point(11, 13))
part1('input.txt')
    