import re

input_lines = [
    "clients: 23.05",
    "clients: 2024-12-01",
    "clients: 2024-12-01 / 2025-12-01",
    "orders: 2017",
    "cats: 2019-10-10",
    "cats & orders: 2019-10-10",
    "cats - orders: 2024-12-01 / 2025-12-01"
]

regex = r'([\w\s]+)[\s]*:[\s]*([-\d\s/:&]+)'

results = []
for line in input_lines:
    match = re.match(regex, line)
    if match:
        key = match.group(1).strip().split()
        value = match.group(2).strip().split()
        results.append((key, value))

print(results)
