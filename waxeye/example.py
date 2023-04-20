from waxeye.parser import Parser
from waxeye import EOF

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

def date_range_parser(left, _, right):
    return DateRangeNode([left, right])

def and_expr_parser(left, _, right):
    return AndExprNode([left, '&', right])

def minus_expr_parser(left, _, right):
    return MinusExprNode([left, '-', right])

# Define the Waxeye grammar
grammar_definition = '''
    start <- pair* EOF ;
    pair <- key ':' value '\n' ;
    key <- /[a-zA-Z_][a-zA-Z0-9_]*/ ;
    value <- float / integer / date_range / date / and_expr / minus_expr / /.+/ ;
    float <- /[0-9]+\.[0-9]+/ {return float_parser($1)} ;
    integer <- /[0-9]+/ {return integer_parser($1)} ;
    date <- /[0-9]{4}-[0-9]{2}-[0-9]{2}/ {return date_parser($1)} ;
    date_range <- date ' / ' date {return date_range_parser($1, $3)} ;
    and_expr <- value ' & ' value {return and_expr_parser($1, $3)} ;
    minus_expr <- value ' - ' value {return minus_expr_parser($1, $3)} ;
'''

parser = Parser(grammar_definition)

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
        parse_tree = parser.parse(line)
        key, value = parse_tree[0], parse_tree[2]
        results.append((key, value))
    except Exception as e:
        print(f"Error parsing line '{line}': {e}")

print(results)
