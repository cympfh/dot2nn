import sys

from dot2nn.compile.dot import compile_dot
from dot2nn.compile.keras import compile_keras


def compile(graphs, type: str) -> str:
    _compile_func = {
        'dot': compile_dot,
        'keras': compile_keras,
    }
    if type in _compile_func:
        return _compile_func[type](graphs)
    else:
        print(f"Error: Unknown type: {type}", file=sys.stderr)
        return None
