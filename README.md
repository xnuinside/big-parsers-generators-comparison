# big-syntax-parsers-comparisons

Status: In progress. Updates will be available soon.

This repository contains samples for parsing the same input lines using different syntax parser generators and parser combinator libraries in Python.

The purpose of this repository is to demonstrate the differences between parser grammars and how they are defined when working with different libraries.

We aim to create parsers that support a small grammar, which validly parse user input. The input is defined as a table name followed by dates after the ':' symbol.

Imagine that we are creating a data warehousing system for non-engineers, and we have a pseudo language to request data from tables. The '&' symbol means 'AND', the '-' symbol means 'exclude' (by foreign key), and so on.

The parsers should be able to validly parse input lines like these:

```console

    clients: 23.05
    clients: 2024-12-01
    clients: 2024-12-01 / 2025-12-01
    orders: 2017
    cats: 2019-10-10
    cats & orders: 2019-10-10
    cats - orders: 2024-12-01 / 2025-12-01

```
This is a test sample, and our purpose is to compare the parsers. Please do not be harsh on our 'test task' :)

In each example, we expect to send a batch of input lines and receive output in a format like this:

```console 
[(['clients'], [23.05]), (['clients'], ['2024-12-01']), (['clients'], [('2024-12-01', '/', '2025-12-01')]), (['orders'], [2017]), (['cats'], ['2019-10-10']), (['cats', '&', 'orders'], ['2019-10-10']), (['cats', '-', 'orders'], [('2024-12-01', '/', '2025-12-01')])]
```

This repo contains comparison and examples for 18 !!! Python syntax parsers:

1. Lark - https://github.com/lark-parser/lark
2. Parsley - https://parsley.readthedocs.io/en/latest/
3. PLY - http://www.dabeaz.com/ply/
4. PyParsing - https://github.com/pyparsing/pyparsing
5. Parsimonious - https://github.com/erikrose/parsimonious
6. ANTLR4 - https://github.com/antlr/antlr4
7. Lrparsing - https://pypi.org/project/lrparsing/
8. SLY - https://sly.readthedocs.io/en/latest/sly.html#sly-overview
9. pyPEG - https://fdik.org/pyPEG/
10. parse - https://github.com/r1chardj0n3s/parse
11. pyleri - https://github.com/cesbit/pyleri
12. Arpeggio - https://github.com/textX/Arpeggio
13. textX - https://github.com/textX/textX
14. TatSu - https://github.com/neogeny/TatSu
15. Waxeye - https://github.com/waxeye-org/waxeye
16. Pegen - https://github.com/we-like-parsers/pegen

(Parser combinator libraries):

17. Parsec - https://pythonhosted.org/parsec/
18. Parsy - https://github.com/python-parsy/parsy

If you know of any other syntax parsing libraries that are not included in this repository, please feel free to open an issue and provide links to them. We would be happy to add new libraries to the repo and the list.

If you are an owner or experienced user of one of these libraries and have suggestions for making the code more user-friendly or better in any other way, please feel free to open an issue and share your knowledge with us.


### Installation

All versions used in the examples are pinned in the pyproject.toml and poetry.lock files. You can easily install them by running poetry shell followed by poetry install.

The ANTLR library, which is a Java parser generator that can create a parser for Python, needs to be installed manually. Please refer to the README.md file in the antlr/ directory for installation instructions.
