import logging
from collections import deque
from dataclasses import dataclass, replace
from typing import Any, Dict, List, Set

from utils import Point, read_input_by_line, reverse


@dataclass(frozen=True)
class LabeledPoint(Point):
    name: str


@dataclass(frozen=True)
class Portal:
    start: Point
    end: Point


class Grid:
    def __init__(self, filename: str):
        lines = read_input_by_line(filename)

        self.width = len(lines[0])
        self.height = len(lines)
        self.grid = [
            list(line) for line in lines
        ]

    def __getitem__(self, key: Point) -> str:
        return self.grid[key.y][key.x]

    def contains_point(self, point: Point) -> bool:
        """ Determines if the given point exists in this grid"""
        return (point.x >= 0) and (point.x < self.width) and (point.y >= 0) and (point.y < self.height)


def find_open_passages(grid: Grid) -> List[Point]:
    """ Find all open passages in the grid """

    all_nodes = []
    for y in range(grid.height):
        for x in range(grid.width):
            p = Point(x, y)
            if grid[p] == '.':
                all_nodes.append(p)

    return all_nodes


def find_labeled_points(grid: Grid) -> Dict[str, List[Point]]:
    """ Find all open passages with a label attached to them """
    all_labels = {}
    for y in range(grid.height):
        for x in range(grid.width):
            p = Point(x, y)
            q = None
            passage = None
            if grid[p].isalpha():
                for n in p.neighbours(grid.contains_point):
                    if grid[n].isalpha():
                        q = n
                    elif grid[n] == '.':
                        passage = n

                if passage is not None:
                    name = ''.join(sorted([grid[p], grid[q]]))
                    if name in all_labels:
                        all_labels[name].append(passage)
                    else:
                        all_labels[name] = [passage]
    return all_labels


def create_graph(all_nodes: List[Point]) -> Dict[Point, List[Point]]:
    result = {}
    for node in all_nodes:
        neighbours = [neighbour for neighbour in node.neighbours(
            lambda n: n in all_nodes)]
        result[node] = neighbours

    return result


def add_portals_to_graph(graph: Dict[Point, List[Point]], all_labels: Dict[str, List[Point]]):
    for points in all_labels.values():
        if len(points) == 2:
            graph[points[0]].append(points[1])
            graph[points[1]].append(points[0])


def find_shortest_path(graph: Dict[Point, List[Point]], start: Point, end: Point, path=[]):
    dist = {start: [start]}
    q = deque()
    q.append(start)
    while len(q):
        at = q.popleft()
        for next in graph[at]:
            if next not in dist:
                dist[next] = [dist[at], next]
                q.append(next)
    return flatten(dist.get(end))


def flatten(l: List[Any]):
    if l == []:
        return l
    if isinstance(l[0], list):
        return flatten(l[0]) + flatten(l[1:])
    return l[:1] + flatten(l[1:])


def part1(filename: str):
    grid = Grid(filename)
    for line in grid.grid:
        logging.debug(''.join(line))

    all_nodes = find_open_passages(grid)
    logging.debug(f'Found {len(all_nodes)} open passages')

    all_labels = find_labeled_points(grid)
    logging.debug(f'Found {len(all_labels)} labelled points:')
    for label in all_labels:
        logging.debug(f'  {label}: {all_labels[label]}')

    graph = create_graph(all_nodes)
    add_portals_to_graph(graph, all_labels)
    logging.debug('Graph elements:')
    for node in graph:
        logging.debug(f'  {node}: {graph[node]}')

    path = find_shortest_path(graph, all_labels['AA'][0], all_labels['ZZ'][0])
    print(f'Part 1: shortest path ({len(path)-1})')


# part1('day20-test1.txt')
# part1('day20-test2.txt')
part1('day20.txt')
