class Interpreter:
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
                raise NameError(f"Variable '{node.var}' not declared")
            self.symbol_table[node.var] = value

        elif node.type == 'PRINT':
            value = self.eval(node.expr)
            print(value)

        elif node.type == 'BINOP':
            left = self.eval(node.left)
            right = self.eval(node.right)
            if node.op == '+': return left + right
            if node.op == '-': return left - right
            if node.op == '*': return left * right
            if node.op == '/': return left // right

        elif node.type == 'NUMBER':
            return node.value

        elif node.type == 'ID':
            if node.name not in self.symbol_table:
                raise NameError(f"Variable '{node.name}' not declared")
            return self.symbol_table[node.name]

        elif node.type == 'STRING':
            return node.value
