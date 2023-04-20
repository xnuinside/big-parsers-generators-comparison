from parsy import (
    regex, string, seq, sep_by, char_from, decimal_digit,
    generate, ParseError
)
from datetime import date

# Define the parser for the key-value pairs
class FloatNode(float): pass
class IntegerNode(int): pass
class DateNode(str): pass
class DateRangeNode(list): pass
class AndExprNode(list): pass
class MinusExprNode(list): pass

def float_parser(node):
    return FloatNode(float(node))

def integer_parser(node):
    return IntegerNode(int(node))

def date_parser(node):
    return DateNode(node)

def date_range_parser(left, right):
    return DateRangeNode([left, right])

def and_expr_parser(left, right):
    return AndExprNode([left, '&', right])

def minus_expr_parser(left, right):
    return MinusExprNode([left, '-', right])

# Define the Parsy grammar
key = regex(r'[a-zA-Z_][a-zA-Z0-9_]*') + string(':').result(None)
float_val = regex(r'\d+\.\d+').map(float_parser)
integer_val = regex(r'\d+').map(integer_parser)
date_val = regex(r'\d{4}-\d{2}-\d{2}').map(date_parser)
date_range_val = seq(date_val, string(' / '), date_val)
date_range = date_range_val.map(date_range_parser)
and_expr = seq(date_val | float_val | integer_val, string('&'), date_val | float_val | integer_val)
and_expr = and_expr.map(and_expr_parser)
minus_expr = seq(date_val | float_val | integer_val, string('-'), date_val | float_val | integer_val)
minus_expr = minus_expr.map(minus_expr_parser)
value = float_val | integer_val | date_range | date_val | and_expr | minus_expr | regex(r'.+')
pair = key + value
parser = sep_by(pair, string('\n'))

lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

try:
    result = parser.parse(lines)
    results = [(key, value) for key, value in result if value is not None]
    print(results)
except ParseError as err:
    print(f"Error parsing input: {err}")
