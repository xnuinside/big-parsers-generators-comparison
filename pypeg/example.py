from pypeg2 import (
    attr,
    optional,
    parse,
    separated,
    word,
)

# Define the parser for the key-value pairs
class Float(float): pass
class Integer(int): pass
class Date(str): pass
class DateRange(list): pass
class AndExpr(list): pass
class MinusExpr(list): pass

def float(s):
    return Float(s)

def integer(s):
    return Integer(s)

def date(s):
    return Date(s)

def date_range(s):
    return DateRange(s.split('/'))

def and_expr(s):
    return AndExpr(s)

def minus_expr(s):
    return MinusExpr(s)

key = word(regex='[a-zA-Z_][a-zA-Z0-9_]*')
value = attr(Float, r'\d+\.\d+') | attr(Integer, r'\d+') | attr(Date, r'\d{4}-\d{2}-\d{2}') | attr(DateRange, r'\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}') | separated(value, optional(' & ') | ' - ', keep=False)

line = attr('key', key) + ':' + attr('value', value)

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
    result = parse(line, line)
    results.append((result.key, result.value))

print(results)
