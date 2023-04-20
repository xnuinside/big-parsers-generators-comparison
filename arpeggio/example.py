from arpeggio import (
    EOF,
    Optional,
    ParserPython,
    PTNodeVisitor,
    RegExMatch as _,
    ZeroOrMore,
)

# Define the parser for the key-value pairs
class FloatNode(float): pass
class IntegerNode(int): pass
class DateNode(str): pass
class DateRangeNode(list): pass
class AndExprNode(list): pass
class MinusExprNode(list): pass

def float_parser():
    return _(r'\d+\.\d+'), lambda node, _: FloatNode(float(node.value))

def integer_parser():
    return _(r'\d+'), lambda node, _: IntegerNode(int(node.value))

def date_parser():
    return _(r'\d{4}-\d{2}-\d{2}'), lambda node, _: DateNode(node.value)

def date_range_parser():
    def action(node, children):
        start, end = children[0].value, children[2].value
        return DateRangeNode([start, end])
    return date_parser, Optional(_('/'), date_parser), action

def and_expr_parser():
    def action(node, children):
        left, right = children[0], children[2]
        return AndExprNode([left, '&', right])
    return expr_parser, _('&'), expr_parser, action

def minus_expr_parser():
    def action(node, children):
        left, right = children[0], children[2]
        return MinusExprNode([left, '-', right])
    return expr_parser, _('-'), expr_parser, action

key = _(r'[a-zA-Z_][a-zA-Z0-9_]*')
value = (
    float_parser
    | integer_parser
    | date_range_parser
    | date_parser
    | and_expr_parser
    | minus_expr_parser
    | _(r'.+')
)

line = key, ':', value

def parse_value(node):
    if isinstance(node, FloatNode):
        return node
    elif isinstance(node, IntegerNode):
        return node
    elif isinstance(node, DateNode):
        return node.value
    elif isinstance(node, DateRangeNode):
        return tuple(node)
    elif isinstance(node, AndExprNode):
        return tuple(node)
    elif isinstance(node, MinusExprNode):
        return tuple(node)
    else:
        return node.value

class KeyValueVisitor(PTNodeVisitor):
    def visit_line(self, node, children):
        return children

    def visit_key(self, node, children):
        return node.value

    def visit_value(self, node, children):
        return parse_value(children[0])

def parse_line(line):
    parse_tree = parser.parse(line)
    return KeyValueVisitor().visit(parse_tree)

parser = ParserPython(line)

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
    key, value = parse_line(line)
    results.append((key, value))

print(results)
