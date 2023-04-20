from parsley import makeGrammar

# Define the grammar for the key-value pairs
grammar = makeGrammar("""
    start = line+:ls -> [tuple(l) for l in ls]

    line = key:w ':' value:v -> (w, v)

    key = <letterOrUnderscore letterOrUnderscoreOrDigit*>

    value = dateRange
          | date
          | float
          | integer
          | expr

    float = <digit+ '.' digit+>:d -> float(d)

    integer = <digit+>:d -> int(d)

    date = <digit{4} '-' digit{2} '-' digit{2}>:d -> d

    dateRange = date:d1 '/' date:d2 -> (d1, '/', d2)

    andExpr = value:v1 '&' value:v2 -> (v1, '&', v2)

    minusExpr = value:v1 '-' value:v2 -> (v1, '-', v2)

    expr = andExpr | minusExpr
""", {})

# Parse the lines and return the results as a list of tuples
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

results = grammar(lines).start()

print(results)
