from __future__ import annotations
import os
from collections import OrderedDict
from dataclasses import dataclass
from math import atan2, degrees, pi, sqrt
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self): return f'({self.x},{self.y})'

    def distance(self, other_point: Point) -> float:
        return sqrt((other_point.y - self.y)**2 + (other_point.x - self.x)**2)


class AsteroidMap:
    def __init__(self, input: List[str]):
        self.asteroids = set()
        self.max_x = len(input[0]) - 1
        self.max_y = len(input)

        for y, line in enumerate(input):
            for x, column in enumerate(line):
                if column == '#':
                    self.asteroids.add(Point(x, y))

    def calculate_viewing_angles(self, viewing_point) -> Dict[float, List[Point]]:
        other_asteroids = self.asteroids.copy()
        other_asteroids.remove(viewing_point)

        viewing_angles = dict()
        for asteroid in other_asteroids:
            angle = degrees(atan2(asteroid.y - viewing_point.y,
                          asteroid.x - viewing_point.x))
            if angle in viewing_angles:
                viewing_angles[angle].append(asteroid)
            else:
                viewing_angles[angle] = [asteroid]

        return viewing_angles

    def count_visible_asteroids(self, viewing_point: Point) -> int:
        viewing_angles = self.calculate_viewing_angles(viewing_point)
        unique_angles = set(viewing_angles)
        return len(unique_angles)

    def find_best_location_for_ims(self) -> Tuple[int, Point]:
        max_asteroid = None
        max_count = -1
        for asteroid in self.asteroids:
            count = self.count_visible_asteroids(asteroid)
            if count > max_count:
                max_count = count
                max_asteroid = asteroid

        return max_count, max_asteroid

    def visible_asteroids_in_order(self, viewing_point: Point) -> List[Point]:
        viewing_angles = self.calculate_viewing_angles(viewing_point)
        ordered_angles = sorted(viewing_angles)

        starting_point = next(i for i,v in enumerate(ordered_angles) if v >= -90.0)
        remaining_asteroids = self.asteroids.copy()
        remaining_asteroids.remove(viewing_point)
        result = []
        
        i = starting_point
        while len(remaining_asteroids) > 0:
            # TODO: only get nearest asteroid
            for asteroid in sorted(viewing_angles[ordered_angles[i]], key=lambda a: a.distance(viewing_point)):
                if asteroid in remaining_asteroids:
                    result.append(asteroid)
                    remaining_asteroids.remove(asteroid)
                    break

            i += 1
            if (i >= len(ordered_angles)):
                i = 0
        
        return result


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


def part2(filename: str, viewing_point: Point, nth_vaporized: int = -1):
    map = AsteroidMap(read_file(filename))

    asteroids = map.visible_asteroids_in_order(viewing_point)
    print(f'{filename}: {asteroids[nth_vaporized-1]}')
    return asteroids[nth_vaporized-1]


if False:
    assert part1('dummy0.txt') == (8, Point(3, 4))
    assert part1('dummy1.txt') == (33, Point(5, 8))
    assert part1('dummy2.txt') == (35, Point(1, 2))
    assert part1('dummy3.txt') == (41, Point(6, 3))
    assert part1('dummy4.txt') == (210, Point(11, 13))
    part1('input.txt')

if True:
    assert part2('dummy4.txt', Point(11, 13), 1) == Point(11, 12)
    assert part2('dummy4.txt', Point(11, 13), 2) == Point(12, 1)
    assert part2('dummy4.txt', Point(11, 13), 200) == Point(8, 2)
    assert part2('dummy4.txt', Point(11, 13), 299) == Point(11, 1)
    part2('input.txt', Point(20, 19), 200)
# rotation starts at 1/2*pi, downwards to 0, to -pi, than from pi downwards again
