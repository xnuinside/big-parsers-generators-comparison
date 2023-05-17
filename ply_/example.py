import ply.lex as lex
import ply.yacc as yacc
from collections import namedtuple

# Define the lexer tokens
tokens = (
    'KEY',
    'FLOAT',
    'INT',
    'DATE',
    'AND',
    'MINUS',
    'RANGE',
    'COLON'
)

t_ignore = ' \t\n'

def t_KEY(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    print(t)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    print(t)
    return t

def t_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_AND(t):
    r'&'
    return t

def t_COLON(t):
    r':'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_RANGE(t):
    r'\/'
    return t

def t_error(t):
    print(f"Invalid token: {t.value!r}")
    t.lexer.skip(1)

# Define the parser rules
def p_lines(p):
    '''lines : line
             | lines line'''
    p[0] = p[1]

def p_line(p):
    '''line : KEY COLON value'''
    p[0] = (p[1], p[3])

def p_value(p):
    '''value : FLOAT
             | INT
             | DATE
             | DATE RANGE DATE
             | expr'''
    p[0] = p[1]

def p_expr(p):
    '''expr : value AND value
            | value MINUS value'''
    p[0] = (p[2], p[1], p[3])

# Build the lexer and parser
lexer = lex.lex(debug=True)
parser = yacc.yacc(debug=True)

# Parse the lines and return the results as a list of tuples
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

results = []
for line in lines.split('\n'):
    if not line.strip():
        continue
    parsed_data = parser.parse(line.strip())
    if parsed_data:
        key = parsed_data[0]
        value = parsed_data[1]
        results.append((key, value))

print(results)
