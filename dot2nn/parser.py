"""Dot-like language Parser"""
from typing import Any, List, Tuple

import rply

from dot2nn.ast import Edge, Graph, LongEdge, Node

tokens = [
    ('IDENTIFIER', r'[a-zA-Z_][^()\[\]{}=\'"\s:;#]*'),
    ('SEMICOLON', r';'),
    ('ARROW', r'->'),
    ('EQUAL', r'='),
    ('NUMBER', r'\d+'),
    ('DOT', r'\.'),
    ('ASTERISK', r'\*'),
    ('STRING', r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')'),
    # ('PAREN_LEFT', r'\('),
    # ('PAREN_RIGHT', r'\)'),
    ('PAREN_SQUARE_LEFT', r'\['),
    ('PAREN_SQUARE_RIGHT', r'\]'),
    ('PAREN_BRACE_LEFT', r'\{'),
    ('PAREN_BRACE_RIGHT', r'\}'),
]

lg = rply.LexerGenerator()

for token, rule in tokens:
    lg.add(token, rule)

lg.ignore(r'#.*(?=\r|\n|$)')
lg.ignore(r'//.*(?=\r|\n|$)')
lg.ignore(r'\s+')
lexer = lg.build()

pg = rply.ParserGenerator(
    [token for token, _ in tokens],
    precedence=[
        ('left', ['ASTERISK']),
    ]
)


@pg.production('expression : graphs')
def expression_paren(p):
    """Top-level"""
    return p[0]


@pg.production('graphs : graph SEMICOLON graphs')
def graphs_semicolon(p):
    """Graphs

    semicolon separated
    """
    return [p[0]] + p[2]


@pg.production('graphs : graph graphs')
def graphs_space(p):
    """Graphs

    space separated
    """
    return [p[0]] + p[1]


@pg.production('graphs : graph')
def graphs_graph(p):
    """Graphs of a graph"""
    return p


@pg.production('graph : IDENTIFIER PAREN_BRACE_LEFT elements PAREN_BRACE_RIGHT')
def graph(p):
    """Graph expression"""
    name, _, elements, _ = p
    return Graph(name.getstr(), elements)


@pg.production('elements : ')
def elements_empty(p):
    """Inner of a Graph"""
    return []


@pg.production('elements : element SEMICOLON elements')
def elements_semicolon(p):
    """Elements

    semicolon separated
    """
    e, _, es = p
    return [e] + es


@pg.production('elements : element elements')
def elements_space(p):
    """Elements

    space separated
    """
    e, es = p
    return [e] + es


@pg.production('element : node')
def element_node(p) -> Node:
    """Node is element"""
    return p[0]


@pg.production('element : edge')
def element_edge(p) -> Edge:
    """Edge is element"""
    return p[0]


@pg.production('element : longedge')
def element_longedge(p) -> LongEdge:
    """LongEdge is element"""
    return p[0]


@pg.production('node : IDENTIFIER')
def node(p) -> Node:
    """A Node"""
    return Node(p[0].getstr())


@pg.production('node : node PAREN_SQUARE_LEFT attributes PAREN_SQUARE_RIGHT')
def node_attribute(p) -> Node:
    """A Node with attributes"""
    u, _, attributes, _ = p
    return Node(u.name, attributes=attributes)


@pg.production('nodes : IDENTIFIER')
def nodes(p) -> List[Node]:
    """Nodes of a Node"""
    return [Node(p[0].getstr())]


@pg.production('nodes : PAREN_BRACE_LEFT nodes_inner PAREN_BRACE_RIGHT')
def element_nodes(p) -> List[Node]:
    """Nodes surrounded { }"""
    return p[1]


@pg.production('nodes_inner : ')
def nodes_inner_empty(p) -> List[Node]:
    """Nodes of no Node"""
    return []


@pg.production('nodes_inner : IDENTIFIER nodes_inner')
def nodes_inner_space(p) -> List[Node]:
    """Nodes

    space separated
    """
    x, xs = p
    return [Node(x.getstr())] + xs


@pg.production('edge : nodes ARROW nodes')
def edge(p) -> Edge:
    """A Edge

    Example
    -------
    x -> y
    {x y} -> z
    """
    u, _, v = p
    return Edge(source=u, target=v)


@pg.production('edge : edge PAREN_SQUARE_LEFT attributes PAREN_SQUARE_RIGHT')
def edge_attributes(p) -> Edge:
    """A Edge with attributes"""
    e, _, attributes, _ = p
    return Edge(source=e.source, target=e.target, attributes=attributes)


@pg.production('longedge : nodes ARROW nodes ARROW nodes')
def longedge_base(p) -> LongEdge:
    """A LongEdge

    The long edges have 2 or more length

    Example
    -------
    x -> y -> z
    """
    u, _, v, _, w = p
    return LongEdge([u, v, w])


@pg.production('longedge : longedge ARROW nodes')
def longedge_recur(p) -> LongEdge:
    le, _, u = p
    return LongEdge(le.points + [u])


@pg.production('longedge : longedge PAREN_SQUARE_LEFT attributes PAREN_SQUARE_RIGHT')
def longedge_attribute(p) -> LongEdge:
    le, _, attributes, _ = p
    return LongEdge(le.points, attributes=attributes)


@pg.production('attributes : ')
def attributes_empty(p) -> List[Tuple[str, Any]]:
    """Empty Attributes"""
    return []


@pg.production('attributes : attribute attributes')
def attributes_single(p) -> List[Tuple[str, Any]]:
    """Attributes

    space separated
    """
    x, xs = p
    return [x] + xs


@pg.production('attribute : IDENTIFIER EQUAL value')
def attribute(p) -> List[Tuple[str, Any]]:
    """attribute definiution

    Example
    -------
    keyword=value
    """
    name, _, value = p
    return (name.getstr(), value)


@pg.production('value : number')
def value_number(p):
    """number is value"""
    return p[0]


@pg.production('value : IDENTIFIER')
def value_identifier(p):
    """keyword is value"""
    return p[0].getstr()


@pg.production('value : STRING')
def value_string(p):
    """string is value"""
    raw_string = p[0].getstr()[1:-1]
    return bytes(raw_string, 'utf-8').decode('unicode_escape')


@pg.production('number : tuple')
def number_tuple(p):
    """tuple is number"""
    return p[0]


@pg.production('tuple : number ASTERISK number')
def tuple_(p):
    """tuple definition"""
    a, _, b = p
    return (a if type(a) is tuple else (a,)) + (b if type(b) is tuple else (b,))


@pg.production('number : int')
def number_int(p):
    """int is number"""
    return p[0]


@pg.production('int : NUMBER')
def int_num(p):
    """int definition"""
    return int(p[0].getstr())


@pg.production('number : float')
def number_float(p):
    """float is number"""
    return p[0]


@pg.production('float : NUMBER DOT NUMBER')
def float_num_dot_num(p):
    """float definition"""
    a, _, b = p
    return float(f"{a.getstr()}.{b.getstr()}")


@pg.production('float : DOT NUMBER')
def float_dot_num(p):
    """float starts with ."""
    _, b = p
    return float(f"0.{b.getstr()}")


parser = pg.build()


def parse(code):
    """Parse dot code"""
    return parser.parse(lexer.lex(code))
