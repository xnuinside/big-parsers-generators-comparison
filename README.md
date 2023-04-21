# big-syntax-parsers-comparisons

Status: In progress. Updates will be available soon. Funny experiments.

This repository contains samples for parsing the same input lines using different syntax parser generators and parser combinator libraries in Python. I tried to generate them with ChatGPT - and results you can see at the bottow of README

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


Regex (why not?) - people often ask me if it's possible to parse the same input lines using regular expressions;
19. re - https://docs.python.org/3/library/re.html
20. regex - https://pypi.org/project/regex/

If you know of any other syntax parsing libraries that are not included in this repository, please feel free to open an issue and provide links to them. We would be happy to add new libraries to the repo and the list.

If you are an owner or experienced user of one of these libraries and have suggestions for making the code more user-friendly or better in any other way, please feel free to open an issue and share your knowledge with us.


### Installation

All versions used in the examples are pinned in the pyproject.toml and poetry.lock files. You can easily install them by running poetry shell followed by poetry install.

The ANTLR library, which is a Java parser generator that can create a parser for Python, needs to be installed manually. Please refer to the README.md file in the antlr/ directory for installation instructions.


### How to run

After installing the required dependencies, you can run the example.py file in the directory of the parser you want to use by using the standard Python command:

```console

    python re/example.py

```

## OpenAI ChatGPT + Parsers

### ChatGPT 3.5 Results

All of the samples in this repository were generated using the OpenAI ChatGPT model. While I find parsers interesting, I don't have enough time to create the same parser using different libraries manually. Instead, I used the code snippets provided and reviewed them myself. The results of my review can be found at the bottom of each code snippet.

To generate the code snippets, I used the following prompt:
```console
python code with pyparsing library to parse lines: """clients: 23.05
    clients: 2024-12-01
    clients: 2024-12-01 / 2025-12-01
    orders: 2017
    cats: 2019-10-10
    cats & orders: 2019-10-10
    cats - orders: 2024-12-01 / 2025-12-01"""

I want to get as output list of pairs like tuple with all tokens in key and tuple with tokens in values. Symbols like '&', '-', '/' should be as a separate tokens.
```

I provided a description of the output format that I wanted to receive, and then used the OpenAI ChatGPT model to generate code snippets for different parser libraries. 

While some of the code snippets worked as expected, some did not. 

I am currently working on fixing the code snippets that didn't work.

List of 'failed' ChatGPT code snippets:

- Ply
- Arpeggio
- lark
- lrparsing
- parse
- parsec
- parsiminious
- parsley
- pegen
- sly
- tatsu
- textx
- waxeye

:D 

- pyparsing - does not failed with errors but don n't parse validly some lines

To put it simply, it seems that ChatGPT was only able to generate valid code for the Python regex library and pure Python's re module. I've had a funny experience with ChatGPT generating code that looked like it would work for a given library, but turned out to be non-functional.

 It's worth noting that if you point out to ChatGPT that its code snippets contain errors, it will simply generate new code based on its own interpretation of the library syntax.


### Chat GPT 4 Results

I attempted a similar approach by comparing the results from ChatGPT 4 and ChatGPT 3.5. However, the generated outputs were quite similar, with both models producing visually close yet ultimately non-functional examples.
