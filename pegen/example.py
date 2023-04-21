from pegen import Parser, ParseError, _flatten
import re

class MyParser(Parser):
    r"""     # Grammar rules
    lines    := line+

    line     := key colon value newline

    key      := ~'[^\:\s]+'
    value    := item | items
    item     := ~'[^\s\-&/]+'
    items    := item (space item)*

    space    := ' '+
    colon    := ':'
    dash     := '-'
    amp      := '&'
    slash    := '/'
    newline  := '\n'
    """

    # Redefine the following methods in your subclass to get useful behavior.
    def error(self, msg):
        raise ParseError(msg, self.pos)

    # Entry point for the parser
    def parse_lines(self, text):
        self.setup(text)
        return self.lines()

    # Grammar rules implementation
    def lines(self):
        return [line for line in self.many(self.line)]

    def line(self):
        key = self.key()
        self.colon()
        value = self.value()
        self.newline()
        return (key, value)

    def key(self):
        return self.expect(self.RE['~\'[^\:\s]+\''])

    def value(self):
        return self.item() | self.items()

    def item(self):
        return self.expect(self.RE['~\'[^\s\-&/]+\''])

    def items(self):
        return _flatten([self.item(), self.many(self.space_item)])

    def space_item(self):
        self.space()
        return self.item()

    def space(self):
        self.expect(' ')

    def colon(self):
        self.expect(':')

    def dash(self):
        self.expect('-')

    def amp(self):
        self.expect('&')

    def slash(self):
        self.expect('/')

    def newline(self):
        self.expect('\n')

    # Lexical analysis
    RE = {
        '~\'[^\:\s]+\'' : re.compile(r'[^\:\s]+'),
        '~\'[^\s\-&/]+\'' : re.compile(r'[^\s\-&/]+')
    }

if __name__ == '__main__':
    parser = MyParser()
    test_text = """clients: 23.05
    clients: 2024-12-01
    clients: 2024-12-01 / 2025-12-01
    orders: 2017
    cats: 2019-10-10
    cats & orders: 2019-10-10
    cats - orders: 2024-12-01 / 2025-12-01"""
    print(parser.parse_lines(test_text))
