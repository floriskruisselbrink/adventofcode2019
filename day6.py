from __future__ import annotations

from typing import List, Set

from utils import read_input_by_line


class Node:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.childs = set()

    def set_parent(self, parent: Node):
        self.parent = parent
        parent.childs.add(self)

    def count_all_parents(self) -> int:
        return len(self.all_parents())

    def all_parents(self) -> Set[Node]:
        parents = set()
        if self.parent:
            parents.add(self.parent)
            parents |= self.parent.all_parents()

        return parents

    def distance(self, parent: Node) -> int:
        distance = 1
        found_parent = self.parent
        while (found_parent != parent):
            distance += 1
            found_parent = found_parent.parent

        return distance

    def __repr__(self):
        return "{}({})".format(self.name, self.count_all_parents())


class OrbitalMap:
    def __init__(self, entries: List[str]):
        self.nodes = {}

        for entry in entries:
            inner, outer = entry.split(')')

            inner_node = self.nodes.get(inner, Node(inner))
            outer_node = self.nodes.get(outer, Node(outer))
            outer_node.set_parent(inner_node)

            self.nodes[inner] = inner_node
            self.nodes[outer] = outer_node

    def count_all_orbits(self) -> int:
        all_orbits = 0
        for node in self.nodes.values():
            all_orbits += node.count_all_parents()

        return all_orbits

    def shortest_path(self, start: Node, destination: Node) -> int:
        common_parents = start.all_parents() & destination.all_parents()
        distance = 99999
        for common_parent in common_parents:
            distance = min(distance, start.distance(
                common_parent) + destination.distance(common_parent))
        return distance


def part1(map: OrbitalMap):
    print("Part 1: {}".format(map.count_all_orbits()))


def part2(map: OrbitalMap):
    start = map.nodes['YOU'].parent
    destination = map.nodes['SAN'].parent
    transfers = map.shortest_path(start, destination)
    print("Part 2: {} (from {} to {})".format(
        transfers, start.name, destination.name))


map = OrbitalMap(read_input_by_line('day6.txt'))
part1(map)
part2(map)
