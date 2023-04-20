from lark import Lark, Transformer

# Define the grammar for the key-value pairs
grammar = """
    start: line+

    line: key ":" value

    key: /[a-zA-Z_][a-zA-Z0-9_]*/

    value: FLOAT -> float
         | INT -> int
         | DATE -> date
         | DATE_RANGE -> date_range
         | expr -> expr

    FLOAT: /\\d+\\.\\d+/
    INT: /\d+/
    DATE: /\d{4}-\d{2}-\d{2}/
    DATE_RANGE: DATE "/" DATE

    expr: value "&" value -> and_expr
        | value "-" value -> minus_expr
"""

# Define the actions for the parser
class KeyValTransformer(Transformer):
    def float(self, value):
        return float(value[0])

    def int(self, value):
        return int(value[0])

    def date(self, value):
        return value[0]

    def date_range(self, value):
        return (value[0], '/', value[2])

    def and_expr(self, value):
        return (value[1], value[0], value[2])

    def minus_expr(self, value):
        return (value[1], value[0], value[2])

# Parse the lines and return the results as a list of tuples
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

parser = Lark(grammar, parser='lalr', transformer=KeyValTransformer())
results = []
for line in lines.split('\n'):
    if not line.strip():
        continue
    parsed_data = parser.parse(line.strip())
    key = parsed_data.children[0].value
    value = parsed_data.children[1]
    results.append((key, value))

print(results)
