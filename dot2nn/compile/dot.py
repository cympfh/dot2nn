from typing import List, Any
from dot2nn.ast import Edge, Graph, Node


class DotCompile:

    def value(self, value: Any) -> str:
        if type(value) is str:
            return repr(value)
        return str(value)

    def node(self, node: Node, context: str, in_edge=False) -> str:
        if in_edge:
            return f"{context}__{node.name}"
        if node.attributes:
            attr = ' '.join(f"{key}={self.value(value)}" for key, value in node.attributes)
            return f"{context}__{node.name} [shape=record label=\"{{ {node.name} | {attr} }}\"]"
        return f"{context}__{node.name} [label=\"{node.name}\"]"

    def nodes(self, nodes: List[Node], context: str, in_edge=True) -> str:
        return f"{{{' '.join(self.node(u, context, in_edge=in_edge) for u in nodes)}}}"

    def edge(self, edge: Edge, context: str) -> str:
        us = edge.source
        vs = edge.target
        x = self.node(us[0], context, True) if len(us) == 1 else self.nodes(us, context, True)
        y = self.node(vs[0], context, True) if len(vs) == 1 else self.nodes(vs, context, True)
        if edge.attributes:
            attr = ' '.join(f"{key}={self.value(value)}" for key, value in edge.attributes)
            return f"{x} -> {y} [label=\"{attr}\"]"
        return f"{x} -> {y}"

    def graph(self, graph: Graph, i: int) -> str:
        context = graph.name

        edges_code = '\n'.join(f"    {self.edge(e, context)};" for e in graph.edges)
        nodes_code = '\n'.join(f"    {self.node(u, context)};" for u in graph.nodes)

        # dummy labeling
        implicit_nodes = set(node.name for e in graph.edges for node in e.source + e.target)
        unused_nodes = implicit_nodes - set(node.name for node in graph.nodes)
        unused_nodes_code = '\n'.join(f"    {self.node(u, context)};"
                                      for u in [Node(name) for name in unused_nodes])

        return f'''  subgraph cluster_{i} {{
    label = "{graph.name}"
{edges_code}
{nodes_code}
{unused_nodes_code}
  }}'''

    def __call__(self, graphs: List[Graph]) -> str:
        graph_code = '\n'.join(f"{self.graph(g, i)}" for i, g in enumerate(graphs))
        return f"""digraph NNGraph {{
{graph_code}
}}"""


def compile_dot(graphs: List[Graph]) -> str:
    return DotCompile()(graphs)
