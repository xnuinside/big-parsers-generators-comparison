from pyleri import (
    Choice,
    Grammar,
    Keyword,
    Node,
    Regex,
    Sequence,
    String,
    Word,
)

# Define the parser for the key-value pairs
class Float(float): pass
class Integer(int): pass
class Date(str): pass
class DateRange(list): pass
class AndExpr(list): pass
class MinusExpr(list): pass

def float_parser(element):
    element.result = Float(element.string)

def integer_parser(element):
    element.result = Integer(element.string)

def date_parser(element):
    element.result = Date(element.string)

def date_range_parser(element):
    start, end = element.string.split('/')
    element.result = DateRange([start, end])

def and_expr_parser(element):
    left, right = element.children
    element.result = AndExpr([left.result, '&', right.result])

def minus_expr_parser(element):
    left, right = element.children
    element.result = MinusExpr([left.result, '-', right.result])

key = Regex(r'[a-zA-Z_][a-zA-Z0-9_]*')
value = Choice(
    Float() <= Regex(r'\d+\.\d+'),
    Integer() <= Regex(r'\d+'),
    Date() <= Regex(r'\d{4}-\d{2}-\d{2}'),
    DateRange() <= Regex(r'\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}'),
    Sequence(AndExpr(), Keyword('&'), AndExpr(), action=and_expr_parser),
    Sequence(MinusExpr(), Keyword('-'), MinusExpr(), action=minus_expr_parser),
    String() <= Regex(r'.+'),
    skip=True
)

line = Sequence(
    Word(key, node_class=Node),
    Keyword(':'),
    Word(value, node_class=Node)
)

grammar = Grammar(line)

lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

results = []
for line in lines.split('\n'):
    if line.strip() == '':
        continue
    parse_tree = grammar.parse(line)
    key = parse_tree.children[0].string
    value = parse_tree.children[2].result
    results.append((key, value))

print(results)
