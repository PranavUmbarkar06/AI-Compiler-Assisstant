<!-- TITLE -->
<h1 align="center">AI Compiler Assistant</h1>

<p align="center">
  A smart, interactive compiler for a custom programming language —  
  complete with lexing, parsing, evaluation, and AI-powered auto-correction.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Custom%20DSL-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20JS%20%7C%20CodeMirror-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Backend-Python-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/AI-LLM%20Error%20Correction-orange?style=for-the-badge">
</p>

---

## Overview

The **AI Compiler Assistant** is a browser-based development environment that:

- Lexes, parses and evaluates a custom programming language  
- Provides **AI-generated corrections, explanations, and optimizations**  
- Shows a beautifully styled **Corrected Code Box**  
- Lets users **auto-replace** their code with a single button  
- Includes a full Python backend + CodeMirror editor frontend

---

# Custom Programming Language

Example:

```txt
integer a = 10;
a = a + 5;
print(a);
```

# Grammar 
- PROGRAM     → STMT_LIST EOF
- STMT_LIST   → (STMT)*
- STMT        → DECL | ASSIGN | PRINT_STMT
- DECL        → "integer" ID "=" EXPR ";" 
- ASSIGN      → ID "=" EXPR ";"
- PRINT_STMT  → "print" "(" EXPR ")" ";"
- EXPR        → TERM { ("+" | "-") TERM }
- TERM        → FACTOR { ("*" | "/") FACTOR }
- FACTOR      → NUMBER | STRING | ID | "(" EXPR ")"

# Backend Architecture

 Backend Architecture (Python)

✔ Lexer – Tokenizes input
✔ Parser – Builds an AST
✔ Evaluator – Executes AST + symbol table
✔ AI Assistant Fallback – On failure, returns:
  - Errors
  - Explanation
  - Fix
  - Optimization
  - Corrected Code

#  Frontend Features (HTML / JS)
- CodeMirror editor (Dracula theme)
- Live output console
- AI assistant panel
- Clean corrected-code UI
- Buttons:
    - Use corrected code → replaces editor
    - Copy code → clipboard support
      
# How to run ? 
Extract this repository into your working directory and simply run the compiler_server.py in webpage directory.




