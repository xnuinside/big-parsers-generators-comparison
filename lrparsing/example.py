from lrparsing import (
    Grammar,
    List,
    LEFT,
    RIGHT,
    ParseError,
    Token,
    TokenRegexp,
    pass_none,
)

# Define the grammar for the key-value pairs
grammar = Grammar(
    r"""
    start : line+ -> [tuple(l) for l in $0]

    line : key ':' value -> ($key, $value)

    key : TOKEN(IDENTIFIER)

    value : float
          | integer
          | date
          | date_range
          | expr

    float : TOKEN(FLOAT) -> float($0)

    integer : TOKEN(INTEGER) -> int($0)

    date : TOKEN(DATE) -> $0

    date_range : date '/' date -> ($date[0], '/', $date[1])

    and_expr : value '&' value -> ($value[0], '&', $value[1])

    minus_expr : value '-' value -> ($value[0], '-', $value[1])

    expr : and_expr | minus_expr

    IDENTIFIER : '[a-zA-Z_][a-zA-Z0-9_]*'

    FLOAT : '\d+\.\d+'

    INTEGER : '\d+'

    DATE : '\d{4}-\d{2}-\d{2}'

    %whitespace : \s+
""",
    {"pass_none": pass_none},
)

# Define custom tokens for the '&' and '-' operators
grammar.add(TOKEN("&", '&'))
grammar.add(TOKEN("-", '-'))

# Define a custom token for the date range separator '/'
grammar.add(TokenRegexp('/', '/'))

# Define a custom token class to handle '&' and '-' tokens
class Op(Token):
    lbp = 10  # operator precedence

    def nud(self):
        raise ParseError(f"Invalid expression: {self.value}")

    def led(self, left):
        return grammar.expr()

    def __repr__(self):
        return self.value

# Set the '&' and '-' tokens to use the Op class
grammar.tokens["&"] = Op
grammar.tokens["-"] = Op

# Parse the lines and return the results as a list of tuples
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

results = grammar.parse(lines).evaluate()

print(results)
