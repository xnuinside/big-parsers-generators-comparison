from lark import Lark, Transformer

# Define the grammar for the key-value pairs
grammar = """
    start: line+

    line: key ":" value

    key: STRING
        | key_expr

    value: STRING -> string
         | FLOAT -> float
         | CALENDAR_DATE -> date
         | INT -> int
         | DATE_RANGE -> date_range
         | expr -> expr

    STRING: /[a-zA-Z_][a-zA-Z0-9_]*/
    
    // Dates
    CALENDAR_DATE : INT "-"? INT "-"? INT
                | INT "-" INT
                | "--" INT "-"? INT

    DATE_RANGE: CALENDAR_DATE " / " CALENDAR_DATE
    expr: value "&" value -> and_expr
            | value "-" value -> minus_expr
    key_expr: key "&" key -> and_expr
            | key "-" key -> minus_expr

    %import common.INT
    %import common.DIGIT
    %import common.FLOAT
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""

# Define the actions for the parser
class KeyValTransformer(Transformer):
    def float(self, value):
        return float(value[0])

    def int(self, value):
        return int(value[0])

    def date(self, value):
        return value[0].value

    def date_range(self, value):
        value = value[0].split()
        return (value[0], '/', value[2])

    def and_expr(self, value):
        return (value[0].children[0].value, '&', value[1].children[0].value)

    def minus_expr(self, value):
        return (value[0].children[0].value, '-', value[1].children[0].value)


# Parse the lines and return the results as a list of tuples
lines = """
clients: 23.05
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
    key = parsed_data.children[0].children[0].children[0]
    if not isinstance(key, tuple):
        key = parsed_data.children[0].children[0].children[0].value

    value = parsed_data.children[0].children[-1]
    results.append((key, value))

print(results)
