from pyparsing import Word, alphas, nums, Literal, Optional, Suppress, Group, delimitedList, LineEnd, oneOf

# Define the grammar for the key-value pairs
key = Word(alphas) + Optional(Word(alphas+'_'))
colon = Suppress(Literal(':'))
float_value = Word(nums+'.').setParseAction(lambda t: float(t[0]))
int_value = Word(nums).setParseAction(lambda t: int(t[0]))
date = Word(nums+'-')
date_range = Group(date + Suppress(Literal('/')) + date)
value = float_value | int_value | date | date_range
line = Group(key + colon + value + LineEnd())

# Define the grammar for the operators
op = oneOf('& -')
expr = value + Optional(Suppress(op) + value)

# Define the grammar for the key with operator
key_expr = key + Group(ampersand | dash + key)

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
    parsed_data = line.strip().parseString(line)
    key_tokens = parsed_data[0].asList()
    value_tokens = expr.parseString(parsed_data[2]).asList()
    results.append((key_tokens, value_tokens))

print(results)
