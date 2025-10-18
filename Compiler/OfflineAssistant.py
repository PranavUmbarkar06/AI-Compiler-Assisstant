import re 
import sys
from Compiler import Lexer,Parser,Evaluator
def _analyze_ast_for_optimizations(node, declared_vars, used_vars):
    """
    Helper function to recursively traverse the AST and collect information.
    This performs a simple data-flow analysis (used vs. declared).
    """
    if not isinstance(node, Parser.ASTNode):
        return

    if node.type == 'DECL':
        declared_vars.add(node.var)
        _analyze_ast_for_optimizations(node.expr, declared_vars, used_vars)

    elif node.type == 'ASSIGN':
        # Don't add to declared_vars, but check if it was declared
        _analyze_ast_for_optimizations(node.expr, declared_vars, used_vars)

    elif node.type == 'ID':
        used_vars.add(node.name)

    # Recurse for all expressions/statements
    elif node.type in ('PROGRAM', 'PRINT'):
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    _analyze_ast_for_optimizations(item, declared_vars, used_vars)
            else:
                _analyze_ast_for_optimizations(value, declared_vars, used_vars)
    
    elif node.type == 'BINOP':
        _analyze_ast_for_optimizations(node.left, declared_vars, used_vars)
        _analyze_ast_for_optimizations(node.right, declared_vars, used_vars)

# -----------------------------------------------------------

def offline_assistant(code: str) -> dict:
    """
    Runs the Mini-C pipeline and returns recommendations or error suggestions.

    Args:
        code: The source code string to analyze.

    Returns:
        A dictionary containing the analysis results, error messages, and suggestions.
    """
    results = {
        'status': 'OK',
        'runtime_output': '',
        'suggestions': [],
        'final_state': None
    }
    
    # 1. Lexical and Syntactic Analysis
    try:
        tokens = Lexer.lexer(code)
        parser = Parser.Parser(tokens)
        ast_tree = parser.parse_program()
        results['suggestions'].append("Lexing and Parsing successful.")
    except SyntaxError as e:
        results['status'] = 'SYNTAX_ERROR'
        results['suggestions'] = [f"**ERROR: Syntax/Lexer Issue** - {e}"]
        return results
    except Exception as e:
        results['status'] = 'COMPILER_ERROR'
        results['suggestions'] = [f"**FATAL ERROR** - An internal parser/lexer issue occurred: {e}"]
        return results

    # 2. Semantic Analysis and Optimization Suggestions (Pre-Interpretation)
    declared_vars = set()
    used_vars = set()
    _analyze_ast_for_optimizations(ast_tree, declared_vars, used_vars)
    
    # Suggestion: Unused variables
    unused_vars = declared_vars - used_vars
    if unused_vars:
        results['suggestions'].append(
            f"**Optimization:** Variable(s) '{', '.join(unused_vars)}' were declared but never used. Consider removing them."
        )
    
    # Suggestion: Constant folding (simple check for BINOP of two NUMBERs)
    # This requires a more complex AST traversal, but for a quick check:
    def check_for_constant_folding(node):
        if node.type == 'BINOP' and node.left.type == 'NUMBER' and node.right.type == 'NUMBER':
            results['suggestions'].append(
                f"**Optimization:** The expression '{node.left.value} {node.op} {node.right.value}' is a constant operation. The compiler could optimize this by calculating the result **({Interpreter().eval(node)})** at compile-time (Constant Folding)."
            )
        if hasattr(node, 'left'): check_for_constant_folding(node.left)
        if hasattr(node, 'right'): check_for_constant_folding(node.right)
        
    check_for_constant_folding(ast_tree)


    # 3. Runtime Analysis (Interpretation)
    try:
        interp = Evaluator.Interpreter()
        # Redirect print output temporarily to capture it
        old_stdout = sys.stdout
        from io import StringIO
        sys.stdout = StringIO()
        
        interp.eval(ast_tree)
        
        # Capture and restore output
        results['runtime_output'] = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        
        results['final_state'] = interp.symbol_table
        
    except (NameError, ZeroDivisionError, TypeError) as e:
        # Runtime errors caught and reported
        sys.stdout = old_stdout # Ensure output is restored even on error
        results['status'] = 'RUNTIME_ERROR'
        error_msg = str(e).replace('Runtime Error: ', '')
        
        if 'not declared' in error_msg:
             results['suggestions'].append(f"**ERROR: Variable Not Declared** - Fix: Ensure '{error_msg.split()[1].strip('\'')}' is declared with 'integer' before assignment or use.")
        elif 'Division by zero' in error_msg:
            results['suggestions'].append(f"**ERROR: Division by Zero** - Fix: Check the value of the divisor in the expression.")
        elif 'Type mismatch' in error_msg:
            results['suggestions'].append(f"**ERROR: Type Mismatch** - Fix: Only 'integer' variables and numbers can be used in arithmetic operations.")
        else:
            results['suggestions'].append(f"**ERROR: Runtime Failure** - {error_msg}")
        return results
    except Exception as e:
        sys.stdout = old_stdout
        results['status'] = 'UNEXPECTED_RUNTIME_ERROR'
        results['suggestions'] = [f"**FATAL RUNTIME ERROR** - An unhandled error occurred: {e}"]
        return results
    
    return results