class ASTNode:
    def __init__(self, type_, **kwargs):
        self.type = type_
        self.__dict__.update(kwargs)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.peek()[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.peek()}")

    def parse_program(self):
        stmts = []
        while self.peek()[0] != 'EOF':
            stmts.append(self.parse_stmt())
        return ASTNode('PROGRAM', statements=stmts)

    def parse_stmt(self):
        tok = self.peek()[0]
        if tok == 'INT':
            return self.parse_decl()
        elif tok == 'ID':
            return self.parse_assign()
        elif tok == 'PRINT':
            return self.parse_print()
        else:
            raise SyntaxError(f"Unexpected token {self.peek()}")

    def parse_decl(self):
        self.eat('INT')
        var_name = self.peek()[1]
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.parse_expr()
        self.eat('SEMICOLON')
        return ASTNode('DECL', var=var_name, expr=expr)

    def parse_assign(self):
        var_name = self.peek()[1]
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.parse_expr()
        self.eat('SEMICOLON')
        return ASTNode('ASSIGN', var=var_name, expr=expr)

    def parse_print(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        var_name = self.peek()[1]
        self.eat('ID')
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return ASTNode('PRINT', var=var_name)

    def parse_expr(self):
        left = self.parse_term()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.peek()[1]
            self.eat(self.peek()[0])
            right = self.parse_term()
            left = ASTNode('BINOP', op=op, left=left, right=right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek()[0] in ('MUL', 'DIV'):
            op = self.peek()[1]
            self.eat(self.peek()[0])
            right = self.parse_factor()
            left = ASTNode('BINOP', op=op, left=left, right=right)
        return left

    def parse_factor(self):
        tok_type, tok_val = self.peek()
        if tok_type == 'NUMBER':
            self.eat('NUMBER')
            return ASTNode('NUMBER', value=int(tok_val))
        elif tok_type == 'ID':
            self.eat('ID')
            return ASTNode('ID', name=tok_val)
        elif tok_type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expr()
            self.eat('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token {self.peek()}")




print('HelloWorld')
