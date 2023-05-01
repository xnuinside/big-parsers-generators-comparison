import re
from parse import (
    compile,
    findall,
)

# Define the parser for the key-value pairs
line_parser = compile("{key}: {value}")

float_parser = compile("{:f}")
integer_parser = compile("{:d}")
date_parser = compile("{year:d}-{month:d}-{day:d}")
date_range_parser = compile("{start:date} / {end:date}")
and_expr_parser = compile("{left} & {right}")
minus_expr_parser = compile("{left} - {right}")

def parse_value(value_str):
    # Try parsing as float, integer, date, date range, and expression
    try:
        result = float_parser.parse(value_str)
        return result[0]
    except:
        pass
    try:
        result = integer_parser.parse(value_str)
        return result[0]
    except:
        pass
    try:
        result = date_parser.parse(value_str)
        return value_str
    except:
        pass
    try:
        result = date_range_parser.parse(value_str)
        return (result['start'], result['end'])
    except:
        pass
    try:
        result = and_expr_parser.parse(value_str)
        return (result['left'], '&', result['right'])
    except:
        pass
    try:
        result = minus_expr_parser.parse(value_str)
        return (result['left'], '-', result['right'])
    except:
        pass
    # If all else fails, return the string
    return value_str

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
    result = line_parser.parse(line)
    key = result['key']
    value = parse_value(result['value'])
    results.append((key, value))

print(results)
