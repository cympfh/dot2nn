import sys

from dot2nn.compile.dot import compile_dot


def compile(graphs, type):
    if type == 'dot':
        return compile_dot(graphs)
    else:
        print(f"Error: Unknown type: {type}", file=sys.stderr)
        return None
