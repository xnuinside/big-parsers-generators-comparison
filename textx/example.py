from textx import (
    metamodel_from_str,
    TextXSemanticError,
)

# Define the parser for the key-value pairs
class FloatNode(float): pass
class IntegerNode(int): pass
class DateNode(str): pass
class DateRangeNode(list): pass
class AndExprNode(list): pass
class MinusExprNode(list): pass

def float_parser(text):
    return FloatNode(float(text))

def integer_parser(text):
    return IntegerNode(int(text))

def date_parser(text):
    return DateNode(text)

def date_range_parser(text):
    start, end = text.split('/')
    return DateRangeNode([start, end])

def and_expr_parser(left, right):
    return AndExprNode([left, '&', right])

def minus_expr_parser(left, right):
    return MinusExprNode([left, '-', right])

def key_value_parser(tokens):
    key, _, value = tokens
    return key, value

grammar_definition = '''
KeyValue: key=ID ':' value=Value ;
Value: Float | Integer | DateRange | Date | AndExpr | MinusExpr | TEXT ;
Float: /\\d+\\.\\d+/ <float_parser> ;
Integer: /\\d+/ <integer_parser> ;
Date: /\\d{4}-\\d{2}-\\d{2}/ <date_parser> ;
DateRange: Date '/' Date <date_range_parser> ;
AndExpr: left=Value 'and' right=Value <and_expr_parser> ;
MinusExpr: left=Value '-' right=Value <minus_expr_parser> ;
ID: /[a-zA-Z_][a-zA-Z0-9_]*/ ;
TEXT: /.+/ ;
'''

metamodel = metamodel_from_str(grammar_definition, classes=[
    FloatNode, IntegerNode, DateNode, DateRangeNode,
    AndExprNode, MinusExprNode
])
metamodel.register_obj_processors({
    'Float': float_parser,
    'Integer': integer_parser,
    'Date': date_parser,
    'DateRange': date_range_parser,
    'AndExpr': and_expr_parser,
    'MinusExpr': minus_expr_parser,
    'KeyValue': key_value_parser,
})

lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats and orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

results = []
for line in lines.split('\n'):
    if line.strip() == '':
        continue
    try:
        parse_tree = metamodel.parse(line)
        key, value = parse_tree.key, parse_tree.value
        results.append((key, value))
    except TextXSemanticError as e:
        print(f"Error parsing line '{line}': {e}")

print(results)
