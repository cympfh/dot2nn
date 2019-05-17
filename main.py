import rply


lg = rply.LexerGenerator()
lg.add('IDENTIFIER', r'[^()\[\]{}=\'"\s;]+')
lg.add('EQUAL', r'=')
lg.add('NUMBER', r'\d+')
lg.add('PLUS', r'\+')
lg.add('PAREN_LEFT', r'\(')
lg.add('PAREN_RIGHT', r'\)')
lg.add('PAREN_SQUARE_LEFT', r'\[')
lg.add('PAREN_SQUARE_RIGHT', r'\]')
lg.add('PAREN_BRACE_LEFT', r'\{')
lg.add('PAREN_BRACE_RIGHT', r'\}')
lg.ignore(r'\s+')
lexer = lg.build()

pg = rply.ParserGenerator(
    ['NUMBER', 'PLUS', 'PAREN_LEFT', 'PAREN_RIGHT'],
    precedence=[
        ('left', ['PLUS']),
    ]
)


class Number(rply.token.BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Add(rply.token.BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() - self.right.eval()


@pg.production('expression : PAREN_LEFT expression PAREN_RIGHT')
def expression_paren(p):
    return p[1]


@pg.production('expression : NUMBER')
def expression_number(p):
    return Number(int(p[0].getstr()))


@pg.production('expression : expression PLUS expression')
def expression_add(p):
    left, _, right = p
    return Add(left, right)


parser = pg.build()


def parse(code):
    return parser.parse(lexer.lex(code)).eval()
