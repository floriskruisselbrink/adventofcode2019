import logging
from collections import deque
from dataclasses import dataclass, replace
from typing import Any, Dict, List, Set

from utils import Point, read_input_by_line, reverse, flatten


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

    def find_open_passages(self) -> List[Point]:
        """ Find all open passages in the grid """

        all_nodes = []
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if self[p] == '.':
                    all_nodes.append(p)

        return all_nodes

    def find_labeled_points(self) -> Dict[str, List[Point]]:
        """ Find all open passages with a label attached to them """
        all_labels = {}
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                q = None
                passage = None
                if self[p].isalpha():
                    for n in p.neighbours(self.contains_point):
                        if self[n].isalpha():
                            q = n
                        elif self[n] == '.':
                            passage = n

                    if passage is not None:
                        name = ''.join(sorted([self[p], self[q]]))
                        if name in all_labels:
                            all_labels[name].append(passage)
                        else:
                            all_labels[name] = [passage]
        return all_labels

    def __getitem__(self, key: Point) -> str:
        return self.grid[key.y][key.x]

    def contains_point(self, point: Point) -> bool:
        """ Determines if the given point exists in this grid"""
        return (point.x >= 0) and (point.x < self.width) and (point.y >= 0) and (point.y < self.height)


class AbstractMaze:
    def __init__(self, nodes: List[Point], labels: Dict[str, List[Point]], graph: Dict[Point, List[Point]] = None):
        self.all_nodes: List[Point] = nodes
        self.all_labels: Dict[str, List[Point]] = labels
        self.graph: Dict[Point, List[Point]] = graph or self.init_graph()

    def clone(self):
        return self.__class__(self.all_nodes, self.all_labels, self.graph)

    def init_graph(self) -> Dict[Point, List[Point]]:
        result = {}
        for node in self.all_nodes:
            neighbours = [neighbour for neighbour in node.neighbours(
                lambda n: n in self.all_nodes)]
            result[node] = neighbours

        return result


class SimpleMaze(AbstractMaze):
    def __init__(self, nodes: List[Point], labels: Dict[str, List[Point]], graph: Dict[Point, List[Point]] = None):
        super().__init__(nodes, labels, graph)

    def init_graph(self):
        result = super().init_graph()

        for points in self.all_labels.values():
            if len(points) == 2:
                result[points[0]].append(points[1])
                result[points[1]].append(points[0])

        return result

    def find_shortest_path(self, start: str, end: str):
        return self._find_shortest_path(self.all_labels[start][0], self.all_labels[end][0])

    def _find_shortest_path(self, start: Point, end: Point, path=[]):
        dist = {start: [start]}
        q = deque()
        q.append(start)
        while len(q):
            at = q.popleft()
            for next in self.graph[at]:
                if next not in dist:
                    dist[next] = [dist[at], next]
                    q.append(next)
        return flatten(dist.get(end))


def part1(filename: str):
    grid = Grid(filename)
    maze = SimpleMaze(grid.find_open_passages(), grid.find_labeled_points())
    path = maze.find_shortest_path('AA', 'ZZ')
    print(f'Part 1: shortest path ({len(path)-1})')


def part2(filename: str):
    grid = Grid(filename)
    maze = SimpleMaze(grid.find_open_passages, grid.find_labeled_points())


# part1('day20-test1.txt')
# part1('day20-test2.txt')
part1('day20.txt')

# part2('day20-test2.txt')
# part2('day20-test3.txt')
# part2('day20.txt')
