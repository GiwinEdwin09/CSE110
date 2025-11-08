## CSE 110 Final Assignment

**Skills:**  
- Python  
- Compiler Design  
- Data Structures  
- Algorithms  

I created a small compiler in Python for C. It can compile small code written in C. As part of the project, I built:

- **Lexical Analyzer:** Breaks the code into tokens, uses regex for pattern matching, and tracks line numbers for error reporting.  
- **Recursive Descent Parser:** Uses symbol table management to handle variables, detects undeclared identifiers and syntax errors, performs type checking and scope handling, and generates an Abstract Syntax Tree (AST).  
- **AST Definition File:** Contains the classes defining the Abstract Syntax Tree structure.  
- **IR Translator:** Translates the resulting AST into an intermediate representation (IR).

_Worked on during UCSC 2025 Spring Quarter (May 14 – June 3)._
