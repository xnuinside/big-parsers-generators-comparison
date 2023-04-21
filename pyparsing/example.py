from pyparsing import Word, alphas, nums, oneOf, Optional, Combine, ParseException
from datetime import datetime

# Define the grammar
key = Word(alphas)
integer = Word(nums)
date = Combine(integer + '-' + integer + '-' + integer)
date_range = date + Optional(oneOf("/ -") + date)
value = (integer | date_range) + Optional(oneOf("& -"))
entry = key + ':' + value

# Define the parser function
def parse_lines(lines):
    parsed_data = []

    for line in lines.split('\n'):
        line = line.strip()
        try:
            parsed_line = entry.parseString(line)
            key_token = parsed_line[0]
            value_tokens = tuple(parsed_line[1:])
            parsed_data.append((key_token, value_tokens))
        except ParseException:
            print(f"Failed to parse line: {line}")

    return parsed_data

# Input lines
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

# Run the parser and print the output
output = parse_lines(lines)
print(output)
