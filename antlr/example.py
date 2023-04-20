from antlr4 import *
from KeyValLexer import KeyValLexer
from KeyValParser import KeyValParser
from KeyValVisitor import KeyValVisitor

# Define the actions for the parser
class KeyValVisitorImpl(KeyValVisitor):
    def visitLine(self, ctx:KeyValParser.LineContext):
        key = ctx.key().getText()
        value = self.visit(ctx.value())
        return (key, value)

    def visitValue(self, ctx:KeyValParser.ValueContext):
        if ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.DATE():
            return ctx.DATE().getText()
        elif ctx.DATE_RANGE():
            date1 = ctx.DATE()[0].getText()
            date2 = ctx.DATE()[1].getText()
            return (date1, '/', date2)
        elif ctx.expr():
            return self.visit(ctx.expr())

    def visitExpr(self, ctx:KeyValParser.ExprContext):
        op = ctx.op.text
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return (left, op, right)

# Parse the lines and return the results as a list of tuples
lines = """clients: 23.05
clients: 2024-12-01
clients: 2024-12-01 / 2025-12-01
orders: 2017
cats: 2019-10-10
cats & orders: 2019-10-10
cats - orders: 2024-12-01 / 2025-12-01"""

input_stream = InputStream(lines)
lexer = KeyValLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = KeyValParser(stream)
tree = parser.start()

visitor = KeyValVisitorImpl()
results = []
for line in tree.line():
    key, value = visitor.visit(line)
    results.append((key, value))

print(results)
