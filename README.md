# big-syntax-parsers-comparisons

Status: In progress. Updates will be available soon. Funny experiments.

Examples, that works well right now*:

- lark_/
- re_/
- regex_/
  
\* story about how I tried ChatGPT & failed - at the bottom of the readme
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

This repo contains comparison and examples for 16 syntax parsers (generators) libraries + 2 examples with regexp:

| No. | Name         | URL                                      | Parsing Algorithms              | Grammar Types               |
|-----|--------------|------------------------------------------|---------------------------------|------------------------------|
| 1   | Lark         | https://github.com/lark-parser/lark      | Earley, LALR, CYK               | EBNF, LALR                  |
| 2   | Parsley      | https://parsley.readthedocs.io/en/latest/| PEG                             | PEG                          |
| 3   | PLY          | http://www.dabeaz.com/ply/               | Lex, Yacc                       | LALR(1)                      |
| 4   | PyParsing    | https://github.com/pyparsing/pyparsing   | Top-down                        | Top-down                     |
| 5   | Parsimonious | https://github.com/erikrose/parsimonious | PEG                             | PEG                          |
| 6   | ANTLR4       | https://github.com/antlr/antlr4          | LL(*)                           | LL(*)                        |
| 7   | Lrparsing    | https://pypi.org/project/lrparsing/      | LR(1)                           | LR(1)                        |
| 8   | SLY          | https://sly.readthedocs.io/en/latest/sly.html#sly-overview | Lex, Yacc | LALR(1)                |
| 9   | pyPEG        | https://fdik.org/pyPEG/                  | PEG                             | PEG                          |
| 10  | parse        | https://github.com/r1chardj0n3s/parse    | -                               | -                            |
| 11  | pyleri       | https://github.com/cesbit/pyleri         | PEG                             | PEG                          |
| 12  | Arpeggio     | https://github.com/textX/Arpeggio        | PEG                             | PEG                          |
| 13  | textX        | https://github.com/textX/textX           | -                               | Domain-Specific Languages    |
| 14  | TatSu        | https://github.com/neogeny/TatSu         | PEG                             | PEG, EBNF                    |
| 15  | Waxeye       | https://github.com/waxeye-org/waxeye      | PEG                             | PEG                          |
| 16  | Pegen        | https://github.com/we-like-parsers/pegen  | PEG                             | PEG                          |

Regex (why not?) - people often ask me if it's possible to parse the same input lines using regular expressions; Configparser, for example, written only with regex.
1. re - https://docs.python.org/3/library/re.html
2. regex - https://pypi.org/project/regex/

If you know of any other syntax parsing libraries that are not included in this repository, please feel free to open an issue and provide links to them. We would be happy to add new libraries to the repo and the list.

If you are an owner or experienced user of one of these libraries and have suggestions for making the code more user-friendly or better in any other way, please feel free to open an issue and share your knowledge with us.


### Parsing Grammars Types
Table generated by ChatGPT - I will review it and correct soon.

| Grammar Name | Meaning                                 | Short Description                                                                                         | URL                                                       |
|--------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| EBNF         | Extended Backus–Naur Form               | A notation for context-free grammars, often used to describe syntax in programming languages and protocols | [Wikipedia](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) |
| LALR         | Look-Ahead Left-to-right, Rightmost derivation | A simplified version of LR grammars that reduces memory requirements and speeds up parsing                | [Wikipedia](https://en.wikipedia.org/wiki/LALR_parser) |
| PEG          | Parsing Expression Grammar              | A type of recognizer for formal languages that provides a simpler and more powerful alternative to CFGs    | [Wikipedia](https://en.wikipedia.org/wiki/Parsing_expression_grammar) |
| Context-Free | -                                       | A grammar that can generate an infinite number of strings from a finite set of rules                      | [Wikipedia](https://en.wikipedia.org/wiki/Context-free_grammar) |
| LALR(1)      | Look-Ahead Left-to-right, Rightmost derivation with 1 lookahead | A variant of LALR grammars that uses a single lookahead token to decide which rule to apply                | [Wikipedia](https://en.wikipedia.org/wiki/LALR_parser#LALR.281.29_parsers) |
| Top-down     | -                                       | A parsing strategy that starts with the root rule and builds the parse tree downwards                     | [Wikipedia](https://en.wikipedia.org/wiki/Top-down_parsing) |
| LL(*)        | Left-to-right, Leftmost derivation (*)  | A type of top-down parser that can handle a wide range of context-free grammars                            | [ANTLR4 Wiki](https://github.com/antlr/antlr4/blob/master/doc/faq/general.md#what-is-ll) |
| LR(1)        | Left-to-right, Rightmost derivation with 1 lookahead | A powerful bottom-up parsing algorithm that can handle a wide range of grammars                           | [Wikipedia](https://en.wikipedia.org/wiki/LR_parser) |
| DSL          | Domain-Specific Language                | A specialized language designed for a specific application domain                                         | [Wikipedia](https://en.wikipedia.org/wiki/Domain-specific_language) |

### Parsing Alghoritms
Table generated by ChatGPT - I will review it and correct soon.


| Parsing Algorithm Name | Meaning                                 | URL                                                                                     | Grammar Type    |
|------------------------|-----------------------------------------|-----------------------------------------------------------------------------------------|-----------------|
| Earley                 | Earley's parsing algorithm             | [Wikipedia](https://en.wikipedia.org/wiki/Earley_parser)                               | EBNF            |
| LALR                   | Look-Ahead Left-to-right, Rightmost derivation | [Wikipedia](https://en.wikipedia.org/wiki/LALR_parser)                                 | LALR, LALR(1)   |
| CYK                    | Cocke-Younger-Kasami algorithm         | [Wikipedia](https://en.wikipedia.org/wiki/CYK_algorithm)                               | Context-Free    |
| PEG                    | Parsing Expression Grammar             | [Wikipedia](https://en.wikipedia.org/wiki/Parsing_expression_grammar)                  | PEG             |
| Lex                    | Lexical analyzer generator             | [Wikipedia](https://en.wikipedia.org/wiki/Lex_(software))                              | LALR(1)         |
| Yacc                   | Yet Another Compiler-Compiler          | [Wikipedia](https://en.wikipedia.org/wiki/Yacc)                                        | LALR(1)         |
| Top-down               | Top-down parsing strategy              | [Wikipedia](https://en.wikipedia.org/wiki/Top-down_parsing)                            | Top-down        |
| LL(*)                  | Left-to-right, Leftmost derivation (*) | [ANTLR4 Wiki](https://github.com/antlr/antlr4/blob/master/doc/faq/general.md#what-is-ll) | LL(*)           |
| LR(1)                  | Left-to-right, Rightmost derivation with 1 lookahead | [Wikipedia](https://en.wikipedia.org/wiki/LR_parser)                                   | LR(1)           |


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
