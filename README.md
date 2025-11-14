AI Compiler Assistant

An interactive web-based compiler assistant that can lex, parse, and evaluate a custom programming language, while also providing AI-powered error detection, explanations, and auto-correction.

The project includes:

A Python backend (lexer, parser, evaluator + AI assistant fallback).

A CodeMirror-powered web editor.

A smart UI that highlights errors, shows detailed explanations, and displays the corrected code in a clean “techy” code box.

A one-click “Use corrected code” replacement button with confirmation.

#Features
🧠 Custom Programming Language

The compiler understands a simple language with:

integer a = 10;
a = a + 5;
print(a);


Grammar:

PROGRAM     → STMT_LIST EOF
STMT_LIST   → (STMT)*
STMT        → DECL | ASSIGN | PRINT_STMT
DECL        → "integer" ID "=" EXPR ";" 
ASSIGN      → ID "=" EXPR ";"
PRINT_STMT  → "print" "(" EXPR ")" ";"
EXPR        → TERM { ("+" | "-") TERM }
TERM        → FACTOR { ("*" | "/") FACTOR }
FACTOR      → NUMBER | STRING | ID | "(" EXPR ")"


Backend (Python)

Lexer – Tokenizes the source code.

Parser – Builds an AST based on grammar.

Evaluator – Executes the AST and manages a symbol table.

AI Assistant Fallback
If parsing fails, the program sends the code to an AI model which returns:

Errors

Explanation

Fix

Optimization

Corrected Code

Incase offline... rule based grammar checking happens using offline assistant

Frontend (HTML + JS)

Output panel shows runtime results

Assistant panel shows AI feedback

Corrected Code Box automatically extracts, sanitizes, and displays only the corrected code

Buttons:

Use corrected code → replaces editor after confirmation

Copy → copies corrected code to clipboard
How to use
1. Run the backend server

simply run compiler_server.py in your terminal. Html file will automatically open in your browser.


2. 


Project Structure
/Compiler
    Lexer.py
    Parser.py
    Evaluator.py
    OnlineAssistant.py
    OfflineAssistant.py
/WebPage
    index.html
    compiler_server.py
    styles.css
main.py
README.md



How the AI Correction System Works

You run code.

If the compiler succeeds → output is shown normally.

If compiler fails:

A detailed error trace is returned.

The code is sent to the AI helper.

AI replies with:

detected problems

corrected code

The frontend extracts only the corrected code.

The corrected code appears inside:

┌─────────────────────────────┐
│ Corrected Code              │
├─────────────────────────────┤
│ integer a = 5;              │
│ print(a);                   │
└─────────────────────────────┘


You can choose to replace your editor code or copy it.

Technologies Used
Backend - Python

Custom lexer, parser, interpreter

Gemini/LLM-based correction

Flask web hosting

Frontend

DOMPurify #reads code from ai generated response

HTML/CSS (custom theme)

Extending the Project

You can easily expand:

✔ Add new keywords

Modify the grammar in Parser.py.

✔ Add new operators

Extend the lexer token rules.

✔ Add new AI correction styles

Modify system_instruction in main.py.



Author

Pranav Umbarkar, Manish Mahato, Ritik Mistry
2025 · AI Compiler Assistant Project