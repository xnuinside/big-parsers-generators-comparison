import parsimonious

# Define the grammar for the key-value pairs
grammar = """
line = key colon value
key = ~"[a-zA-Z_][a-zA-Z0-9_]*"
colon = ":"
float = ~"\d+\.\d+"
int = ~"\d+"
date = ~"\d{4}-\d{2}-\d{2}"
date_range = date "/" date
value = float / int / date / date_range / expr
expr = value op value
op = ("&" / "-")
"""

# Define the actions for the parser
class LineVisitor(parsimonious.NodeVisitor):
    def visit_line(self, node, visited_children):
        return (visited_children[0], visited_children[2])
    
    def visit_key(self, node, visited_children):
        return node.text
    
    def visit_float(self, node, visited_children):
        return float(node.text)
    
    def visit_int(self, node, visited_children):
        return int(node.text)
    
    def visit_date(self, node, visited_children):
        return node.text
    
    def visit_date_range(self, node, visited_children):
        return (visited_children[0], '/', visited_children[2])
    
    def visit_value(self, node, visited_children):
        return visited_children[0]
    
    def visit_expr(self, node, visited_children):
        return (visited_children[1], visited_children[0], visited_children[2])
    
    def visit_op(self, node, visited_children):
        return node.text

# Parse the lines and return the results as a list of tuples
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

parser = parsimonious.Grammar(grammar)
visitor = LineVisitor()

results = []
for line in lines.split('\n'):
    if not line.strip():
        continue
    parsed_data = parser.parse(line.strip())
    key = visitor.visit(parsed_data.children[0])
    value = visitor.visit(parsed_data.children[2])
    results.append((key, value))

print(results)
