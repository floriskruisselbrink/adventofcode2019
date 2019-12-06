import os
from typing import List

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')
dummy_file = os.path.join(os.path.dirname(__file__), 'dummy.txt')


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.childs = set()

    def set_parent(self, parent):
        self.parent = parent
        parent.childs.add(self)

    def count_all_parents(self):
        if self.parent:
            return 1 + self.parent.count_all_parents()
        else:
            return 0
    
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
    
    def count_all_orbits(self):
        all_orbits = 0
        for node in self.nodes.values():
            all_orbits += node.count_all_parents()
        
        return all_orbits

def part1():
    with open(input_file) as input:
        map = OrbitalMap(input.read().splitlines())
        print(map.nodes)
        print("Part 1: {}".format(map.count_all_orbits()))

part1() # 1674 is too low
                
    

