import os
from dataclasses import dataclass
from typing import List, Set, Tuple
from math import gcd

DEBUG = False


@dataclass(frozen=True)
class Asteroid:
    x: int
    y: int

    def __repr__(self):
        return f'({self.x},{self.y})'


class AsteroidMap:
    def __init__(self, textinput: List[str]):
        self.asteroids = set()
        self.max_x = len(textinput[0])-1
        self.max_y = len(textinput)

        for y, line in enumerate(textinput):
            for x, point in enumerate(line):
                if point == '#':
                    self.asteroids.add(Asteroid(x, y))

    def max_visible_asteroids(self) -> Tuple[Asteroid, int]:
        asteroid = None
        max_count = 0
        for a in self.asteroids:
            count = self.count_visible_asteroids(a)
            if count > max_count:
                asteroid = a
                max_count = count

            if DEBUG:
                print(f'{a}: visible asteroids: {count}')

        return (asteroid, max_count)

    def count_visible_asteroids(self, viewing_point: Asteroid) -> int:
        visible_asteroids = self.asteroids.copy()
        visible_asteroids.remove(viewing_point)

        # for each asteroid, find all asteroids obscured by it
        invisible_points = set()
        for a in visible_asteroids:
            invisible_points |= self.find_blocked_points(viewing_point, a)

        if DEBUG:
            invisible_asteroids = invisible_points & visible_asteroids
            invisible_str = ', '.join(map(str, invisible_asteroids))
            print(f'{viewing_point}: invisible asteroids: {invisible_str}')

        visible_asteroids -= invisible_points
        return len(visible_asteroids)

    """ Find all points within the grid that are blocked by second, as seen from first """
    def find_blocked_points(self, first: Asteroid, second: Asteroid) -> Set[Asteroid]:
        delta_x = second.x - first.x
        delta_y = second.y - first.y

        divisor = gcd(delta_x, delta_y)
        
        if delta_x != 0:
            delta_x = delta_x // divisor
        if delta_y != 0:
            delta_y = delta_y // divisor

        next_x = second.x + delta_x
        next_y = second.y + delta_y
        blocked = set()
        while (next_x >= 0) and (next_y >= 0) and (next_x <= self.max_x) and (next_y <= self.max_y):
            blocked.add(Asteroid(next_x, next_y))
            next_x += delta_x
            next_y += delta_y

        if DEBUG and (len(blocked) > 0):
            blocked_str = ', '.join(map(str, blocked))
            print(f'{first} - {second}: blocked points {blocked_str}')

        return blocked


def part1(filename: str) -> Tuple[Asteroid, int]:
    input_file = os.path.join(os.path.dirname(__file__), filename)
    with open(input_file) as input:
        map = AsteroidMap(input.read().splitlines())

    if DEBUG:
        print(f'Number of asteroids: {len(map.asteroids)}')

    asteroid, max_count = map.max_visible_asteroids()
    print(f'Part 1 ({filename}): Asteroid{asteroid} visible: {max_count}')
    return (asteroid, max_count)


assert part1('dummy0.txt') == (Asteroid(3,4), 8)
assert part1('dummy1.txt') == (Asteroid(5,8), 33)
assert part1('dummy2.txt') == (Asteroid(1,2), 35)
assert part1('dummy3.txt') == (Asteroid(6,3), 41)
assert part1('dummy4.txt') == (Asteroid(11,13), 210)
part1('input.txt')
