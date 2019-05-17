from typing import List

from rply.token import BaseBox


class Node(BaseBox):

    def __init__(self, name, attributes=None):
        self.name: str = name
        self.attributes = attributes

    def __repr__(self):
        return f"Node(name={self.name} attributes={self.attributes})"


class Edge(BaseBox):

    def __init__(self, source, target, attributes=[]):
        self.source: List[Node] = source
        self.target: List[Node] = target
        self.attributes = attributes

    def __repr__(self):
        return f"Edge({self.source} -> {self.target} attributes={self.attributes})"


class Graph(BaseBox):

    def __init__(self, name, elements):
        self.name = name
        self.nodes = []
        self.edges = []
        for e in elements:
            if type(e) == Node:
                self.nodes.append(e)
            elif type(e) == Edge:
                self.edges.append(e)

    def __repr__(self):
        return f"Graph(name={self.name} nodes={self.nodes} edges={self.edges})"
