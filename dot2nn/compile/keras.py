from typing import List

from dot2nn.ast import Edge, Graph, Node


class Keras:

    @classmethod
    def is_sequential(cls, graph: Graph) -> bool:
        """The graph can be write as a Sequential model?"""
        return True  # TODO

    def layer(self, edge: Edge) -> str:
        """Layer code
        """
        net = edge.attributes.get('net', 'linear')
        if net == 'linear':
            return 'Dense()'
        return '???'

    def graph_sequential(self, graph: Graph) -> str:
        code = []
        model_name = graph.name
        code.append(f"{model_name} = Sequential()")

        defined = set(['Input'])
        num_edges = len(graph.edges)
        used = [False] * num_edges
        while 'Output' not in defined:
            for i, e in enumerate(graph.edges):
                if used[i]:
                    continue
                code.append(f"{model_name}.add({self.layer(e)})")
                for u in e.target:
                    defined.add(u.name)
                used[i] = True

        return '\n'.join(code)

    def graph(self, graph: Graph) -> str:
        if Keras.is_sequential(graph):
            return self.graph_sequential(graph)
        else:
            return self.graph_model(graph)

    def __init__(self, graphs: List[Graph]):
        self.graphs = graphs

    def __call__(self) -> str:
        return '\n\n'.join(self.graph(graph) for graph in self.graphs)


def compile_keras(graphs):
    return Keras(graphs)()
