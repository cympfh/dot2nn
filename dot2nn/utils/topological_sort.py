from typing import List

from dot2nn.ast import Edge, Graph, Node


class TopologicalSort:

    def visit(self,
              u: int,
              used: List[bool],
              rd: List[List[int]],
              order: List[int]):
        if used[u]:
            return
        used[u] = True
        for v in rd[u]:
            self.visit(v, used, rd, order)
        order.append(u)

    def sort(self, neigh: List[List[int]]) -> List[int]:
        n = len(neigh)
        rd = [[] for _ in range(n)]
        for u in range(n):
            for v in neigh[u]:
                rd[v].append(u)
        used = [False] * n
        order = []
        for u in range(n):
            self.visit(u, used, rd, order)
        return order

    def register_nodes(self, graph: Graph):
        self.node2idx = {}
        self.idx2node = []
        for e in graph.edges:
            for u in e.source + e.target:
                if u not in self.idx2node:
                    idx = len(self.idx2node)
                    self.node2idx[u] = idx
                    self.idx2node.append(u)

    def __init__(self, graph: Graph):
        self.register_nodes(graph)
        n = len(self.idx2node)
        neigh = [[] for _ in range(n)]
        for e in graph.edges:
            for u in e.source:
                for v in e.target:
                    neigh[self.node2idx[u]].append(self.node2idx[v])

        order = self.sort(neigh)
        self.order = [self.idx2node[i] for i in order]


g = Graph('g', [
    Edge([Node('Input')], [Node('x'), Node('y')]),
    Edge([Node('x'), Node('y')], [Node('z')]),
    Edge([Node('z')], [Node('Output')]),
])
print(TopologicalSort(g).order)
