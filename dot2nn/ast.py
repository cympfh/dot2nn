from typing import List, Union

from rply.token import BaseBox


class Node(BaseBox):

    def __init__(self, name: str, attributes=None):
        self.name = name
        self.attributes = attributes

    def __repr__(self):
        return f"Node(name={self.name} attributes={self.attributes})"


class Edge(BaseBox):

    def __init__(self, source: List[Node], target: List[Node], attributes=[]):
        self.source = source
        self.target = target
        self.attributes = attributes

    def __repr__(self):
        return f"Edge({self.source} -> {self.target} attributes={self.attributes})"


class LongEdge(BaseBox):

    def __init__(self, points: List[List[Node]], attributes=[]):
        self.points = points
        self.attributes = attributes

    def __repr__(self):
        return f"LongEdge({self.points} attributes={self.attributes}"


class Graph(BaseBox):

    def __init__(self, name: str, elements: List[Union[Node, Edge, LongEdge]]):
        self.name = name
        self.nodes = []
        self.edges = []
        for e in elements:
            if type(e) == Node:
                self.nodes.append(e)
            elif type(e) == Edge:
                self.edges.append(e)
            elif type(e) == LongEdge:
                m = len(e.points)
                for i in range(m - 1):
                    self.edges.append(Edge(e.points[i], e.points[i + 1], e.attributes))

    def __repr__(self):
        return f"Graph(name={self.name} nodes={self.nodes} edges={self.edges})"
