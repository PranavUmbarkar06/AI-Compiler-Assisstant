class Interpreter:
    # ... (Your Interpreter class implementation remains unchanged)
    def __init__(self):
        self.symbol_table = {}

    def eval(self, node):
        if node.type == 'PROGRAM':
            for stmt in node.statements:
                self.eval(stmt)

        elif node.type == 'DECL':
            value = self.eval(node.expr)
            self.symbol_table[node.var] = value

        elif node.type == 'ASSIGN':
            value = self.eval(node.expr)
            if node.var not in self.symbol_table:
                raise NameError(f"Runtime Error: Variable '{node.var}' not declared")
            self.symbol_table[node.var] = value

        elif node.type == 'PRINT':
            value = self.eval(node.expr)
            print(value)
            return value # Return value for possible future features (like I/O tracking)

        elif node.type == 'BINOP':
            left = self.eval(node.left)
            right = self.eval(node.right)
            
            # Type checking and operation
            if isinstance(left, int) and isinstance(right, int):
                if node.op == '+': return left + right
                if node.op == '-': return left - right
                if node.op == '*': return left * right
                if node.op == '/': 
                    if right == 0:
                         raise ZeroDivisionError("Runtime Error: Division by zero")
                    return left // right # Integer division
            else:
                 raise TypeError(f"Runtime Error: Type mismatch in binary operation '{node.op}' between types {type(left).__name__} and {type(right).__name__}")
        
        elif node.type == 'NUMBER':
            return node.value

        elif node.type == 'ID':
            if node.name not in self.symbol_table:
                raise NameError(f"Runtime Error: Variable '{node.name}' not declared")
            return self.symbol_table[node.name]

        elif node.type == 'STRING':
            return node.value

    def __repr__(self):
        return f"Final Symbol Table: {self.symbol_table}"