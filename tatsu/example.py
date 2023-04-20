from tatsu import grammar, parse
from datetime import date

# Define the parser for the key-value pairs
class FloatNode: pass
class IntegerNode: pass
class DateNode: pass
class DateRangeNode: pass
class AndExprNode: pass
class MinusExprNode: pass

def float_parser(node):
    return FloatNode(float(node))

def integer_parser(node):
    return IntegerNode(int(node))

def date_parser(node):
    year, month, day = node.split('-')
    return DateNode(date(int(year), int(month), int(day)))

def date_range_parser(left, right):
    return DateRangeNode([left, right])

def and_expr_parser(left, right):
    return AndExprNode([left, '&', right])

def minus_expr_parser(left, right):
    return MinusExprNode([left, '-', right])

# Define the TatSu grammar
grammar_definition = '''
    @@grammar::KeyValue

    start = pair*
    pair = key ":" value {result= (key, value)}
    key = /[a-zA-Z_][a-zA-Z0-9_]*/
    value = float | integer | date_range | date | and_expr | minus_expr | /.+/
    date_range = date " / " date {result= date_range_parser(left, right)}
    and_expr = value " & " value {result= and_expr_parser(left, right)}
    minus_expr = value " - " value {result= minus_expr_parser(left, right)}
    float = /\d+\.\d+/ {result= float_parser(_)}
    integer = /\d+/ {result= integer_parser(_)}
    date = /\d{4}-\d{2}-\d{2}/ {result= date_parser(_)}
'''

parser = grammar.compile(grammar_definition)

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
    try:
        parse_tree = parse(parser, line)
        key, value = parse_tree[0], parse_tree[1]
        results.append((key, value))
    except Exception as e:
        print(f"Error parsing line '{line}': {e}")

print(results)
