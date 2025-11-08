CSE 110 Final Assignment

Skills: Python, Compiler Design, Data Structures, Algorithms
I created a small compiler in python for C. It can compile small code in C. As part of the project, I built
	●  Lexical Analyzer that breaks the code down into tokens, uses regexfor pattern matching and also tracks line numbers for error reporting
	●  A recursive descent parser. It uses symbol table management to manage variables. Looks for undeclared identifiers and also syntax errors. It can handle type checking, scope, and also generate an Abstract Syntax Tree of the code.
	●  A file that contains the Abstract syntax tree, defining the classes.
	●  Translates the resulting AST into an IR.
