import re
import sys

# --- LEXER (Token Definition) ---
TOKENS = [
    # CRITICAL FIX: Add rule to SKIP single-line comments starting with #
    ('SKIP', r'#[^\n]*'),
    
    ('INT', r'integer\b'), 
    ('PRINT', r'print\b'),
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
    ('SKIP', r'[\t\n ]+') # Skip whitespace and newlines
]

def lexer(code):
    """Converts source code into a list of (TYPE, VALUE) tokens."""
    pos = 0
    tokens = []
    # Note: Comments and spaces must be processed first to be skipped correctly.
    compiled_tokens = [(t, re.compile(p)) for t, p in TOKENS]
    
    while pos < len(code):
        match = None
        for token_type, regex in compiled_tokens:
            match = regex.match(code, pos)
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