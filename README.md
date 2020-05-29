# parser_generator

## Introduction
This is my take on the parser generator in the style of Bison.

It is not meant to be particularly fast or efficient, it is just meant to crystallize the concepts
of parsing described in Chapter 3 of the 'Dragon Book' [1], hence Python was used as the programming tool.

Parser generator is a tool which takes a specifications of a programming language grammar and creates a parser which
is capable of deciding whether a stream of programming language tokens is syntacticly correct (the parsing process is
usually the second stage of a compiler). 

Writing a parser can be a boring and tedious job (although not as much as writing a lexical analyzer) and it is sometimes
better left to a specialized tool. Parsing essentially boils down to recognizing whether a provided input sentence
conforms to the rules of a programming language grammar.

Result of a parsing process, besides the information whether the parsing was successful, is usually a parse tree.
Parse tree shows syntactic relations of words in a sentence.

## Method
There are many different methods by which a sentence can be parsed. They can be classified in a few ways. Top-down parsers
build the parse tree from the root down to the leaves, while bottom-up parsers build the parse tree from the leaves up.
Some parsers use the rightmost derivation, while others use the leftmost derivation, etc.

A parser generated here is of LR(1) type, where **L** stands for left-to-right input scan, **R** stands for rightmost
derivation in reverse, and **(1)** stands for one symbol of lookahead. Parsers of this type generally have large parsing
tables, so they are a common choice for a parser generator, while some others, like LL(1) parsers, are more suitable for
hand-coding.

### Parsing the input file
Input file contains a specification of the grammar. Grammar is specified using productions which are fed to the
processing functions.

**process_productions.py** does exactly what its name tells us. It looks at the provided production and attaches it to
the specified nonterminal. It also creates the objects which represent terminal and nonterminal grammar symbols, as needed.

After the productions are processed, we have a dictionary of terminal symbols, and one of nonterminal symbols, which are
passed along to the collection creation module.

### Creating the collection of sets of LR(1) items
Item is a construction which tells us how much of a production we have seen at a given point in the parsing process.
By creating sets of LR(1) items, we essentially build states of LR(0) automaton which is used to decide whether the input
sentence is syntacticly correct. This job is done by the **lr1_collection.py** with the help of utility functions from
**first_follow.py**

### Creating the parsing tables
At every step of the parsing process, we encounter the dilemma whether to shift (read) another terminal symbol from the
input stream or perform a reduction (replace the body of the production with its head). Two additional structures help us
with the choice. ACTION table tells us whether to shift or reduce, while GOTO tells us which is the next state of the LR(0)
automaton that should be put on the stack of states. ACTION and GOTO tables are built from the collection of sets of LR(1)
items in **lr1_tables.py**.

### Parser code generation
Now that the tables are created, C++ parser code can be emitted. Parser is presented by the *Parser* class and it contains
definitions of ACTION and GOTO tables. The actual parsing algorithm, as well as all other previously used, are described
in [1].

## Input file description
Input file which contains the language grammar must have an '.mlg' extension.
It must have four distinct sections:
  * Manifest section contains user-written C++ code which will be inserted in the generated lexer's header file as-is.
  It begins with a label '_manifest:'.
  * Types section contains C++ types of the values that the heads of productions can take. Since some user defined code can
  be executed with every reduction, and every grammar symbol can hold some value, types of those values must be collected in
  one place, so a union of types can be generated. This section begins with a label '_types:'.
  * Tokens section should be used to define token types. If this parser generator is used in unison with my lexer generator,
  then the token sections of lexer and parser generators MUST look exactly the same. Furthermore, tokens (terminals) MUST be
  defined in uppercase letters. This section begins with a label '_tokens:'.
  * Grammar section defines the productions of a grammar. Each nonterminal which is the head of a production can be given
  a value type. A piece of C++ code can be associated with every production, which will be executed when that production is
  reduced. Nonterminals MUST be defined in all lowercase letters.
  
User has an option to access the values of the reduced production's head and body symbols by using placeholders.
$$ stands for the value of the head, while $0, $1, $2,... stand for the values of first, second, third,... symbol of
the body.

It should be noted that all the values of grammar symbols should be synthesized and semantic actions can only occur at
the end of the production body (e.g. postfix SDT with and S-attributed SDD).

## Example
All which was previously explained can be seen in action by running the parser generator on the **example.mlg** file
found in the *example/* directory. The file describes syntax-directed translation of simple arithmetic expressions, which
means that the parser can calculate the values of given arithmetic expressions.

**example.cpp** contains the *main()* function of the example program and includes the generated parser's header. The program
calls the parsers to find out whether the sentence in the **example.txt** file is correct, as well as to print the result of
the arithmetic expression.

Header and source files of the lexer, as well as its **.mll** description file, are included in the *example/* folder.

To try this you should:
  * Download the *parser_generator* binary from the *releases* tab of this GitHub page.
  * Run the *parser_generator* binary with **example.mlg** as input file. This will produce header and source files of the
  generated parser (**my_little_parser.h** and **my_little_parser.cpp**).
  * Compile the example program with a compiler which supports C++11 standard.
  
          g++ -std=c++11 my_little_lexer.cpp my_little_parser.cpp example.cpp -O3 -o example.out
          
  * Run the program and see the results!
  
## *TODO* list
* Implement support for ambiguous grammars, using precedence and priorities.
* Implement comprehensive error recovery, as now the parser just halts on error.

## Citations
[1] Aho, A., Sethi, R. & Ullman, J. (1986). Compilers, principles, techniques, and tools.
Reading, Mass: Addison-Wesley Pub. Co.
