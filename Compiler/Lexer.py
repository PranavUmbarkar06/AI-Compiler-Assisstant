import re
import sys

# --- LEXER (Token Definition) ---
TOKENS = [
    ('INT', r'integer\b'), # Added \b for word boundary
    ('PRINT', r'print\b'), # Added \b for word boundary
    ('STRING', r'"[^"]*"'),
    ('NUMBER', r'\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMICOLON', r';'),
    ('SKIP', r'[\t\n ]+')
]

def lexer(code):
    """Converts source code into a list of (TYPE, VALUE) tokens."""
    pos = 0
    tokens = []
    # Pre-compile patterns for minor optimization
    compiled_tokens = [(t, re.compile(p)) for t, p in TOKENS]
    
    while pos < len(code):
        match = None
        for token_type, regex in compiled_tokens:
            match = regex.match(code, pos) # Match from the current position
            if match:
                text = match.group()
                if token_type != 'SKIP':
                    tokens.append((token_type, text))
                pos = match.end()
                break
        if not match:
            # If no token matched, raise an error
            raise SyntaxError(f'Lexer Error: Unexpected character "{code[pos]}" at position {pos}')
    tokens.append(('EOF', ''))
    return tokens