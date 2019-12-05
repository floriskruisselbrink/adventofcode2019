import os
from typing import List, Set, Tuple

Point = Tuple[int, int]

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

def next_point(point: Point, direction: str) -> Point:
    if direction == 'R':
        return (point[0], point[1] + 1)
    elif direction == 'L':
        return (point[0], point[1] - 1)
    elif direction == 'U':
        return (point[0] + 1, point[1])
    elif direction == 'D':
        return (point[0] - 1, point[1])

def read_wire(wire: str) -> List[Point]:
    result = list()
    
    point = (0, 0)
    for instruction in wire.split(','):
        direction = instruction[0]
        distance = int(instruction[1:])

        for i in range(distance):
            point = next_point(point, direction)
            result.append(point)
    
    return result

def manhattan(point: Point) -> int:
    return abs(point[0]) + abs(point[1])

def steps(points: List[Point], intersection: Point) -> int:
    for step, point in enumerate(points):
        if point == intersection:
            return step+1

def part1(input_file: str):
    with open(input_file) as input:
        points1 = read_wire(input.readline())
        points2 = read_wire(input.readline())

        intersections = set(points1) & set(points2)
        distances = [manhattan(p) for p in intersections]
        print("Part 1: {}".format(min(distances)))

def part2(input_file: str):
    with open(input_file) as input:
        points1 = read_wire(input.readline())
        points2 = read_wire(input.readline())

        intersections = set(points1) & set(points2)

        steps1 = [steps(points1, i) for i in intersections]
        steps2 = [steps(points2, i) for i in intersections]

        summed_steps = [i + j for i, j in zip(steps1, steps2)]
        print("Part 2: {}".format(min(summed_steps)))

part1(input_file)
part2(input_file)