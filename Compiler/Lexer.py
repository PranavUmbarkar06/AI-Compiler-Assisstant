import re

TOKENS = [
    ('INT', r'integer'),
    ('PRINT', r'print'),
    ('STRING', r'"[^"]*"'),        # String literals
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
    pos = 0
    tokens = []
    while pos < len(code):
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code[pos:])
            if match:
                text = match.group()
                if token_type != 'SKIP':
                    tokens.append((token_type, text))
                pos += len(text)
                break
        if not match:
            raise SyntaxError(f'Unexpected charecter : {code[pos]}')
    tokens.append(('EOF', ''))
    return tokens
