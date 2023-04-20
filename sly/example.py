from sly import Lexer, Parser

# Define the lexer for the key-value pairs
class KeyValueLexer(Lexer):
    tokens = {IDENTIFIER, FLOAT, INTEGER, DATE, DATE_RANGE, AMPERSAND, HYPHEN, COLON, SLASH}

    ignore = ' \t\r'
    ignore_comment = r'\#.*'

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    FLOAT = r'\d+\.\d+'
    INTEGER = r'\d+'
    DATE = r'\d{4}-\d{2}-\d{2}'
    DATE_RANGE = DATE + r'/' + DATE
    AMPERSAND = r'&'
    HYPHEN = r'-'
    COLON = r':'
    SLASH = r'/'

# Define the parser for the key-value pairs
class KeyValueParser(Parser):
    tokens = KeyValueLexer.tokens

    @_('line')
    def start(self, p):
        return [p.line]

    @_('line line')
    def start(self, p):
        return [p.line0, p.line1]

    @_('IDENTIFIER COLON value')
    def line(self, p):
        return (p.IDENTIFIER, p.value)

    @_('FLOAT')
    def value(self, p):
        return float(p.FLOAT)

    @_('INTEGER')
    def value(self, p):
        return int(p.INTEGER)

    @_('DATE')
    def value(self, p):
        return p.DATE

    @_('DATE_RANGE')
    def value(self, p):
        return tuple(p.DATE_RANGE.split('/'))

    @_('value AMPERSAND value')
    def value(self, p):
        return (p.value0, '&', p.value1)

    @_('value HYPHEN value')
    def value(self, p):
        return (p.value0, '-', p.value1)

    def error(self, p):
        if p:
            raise ValueError(f"Syntax error at {p.type}")
        else:
            raise ValueError("Syntax error at EOF")

# Parse the lines and return the results as a list of tuples
lexer = KeyValueLexer()
parser = KeyValueParser()

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
    tokens = lexer.tokenize(line)
    result = parser.parse(tokens)
    results.append(result)

print(results)
