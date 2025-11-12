import os
import sys

# --- Dynamically add Compiler folder to Python path ---
current_dir = os.path.dirname(os.path.abspath(__file__))
compiler_path = os.path.join(current_dir, "Compiler")

if compiler_path not in sys.path:
    sys.path.append(compiler_path)

# --- Now imports work globally ---
from Compiler import Lexer, Parser, Evaluator



from io import StringIO

def offline_assistant(code: str) -> list:
    """
    Analyze `code` and return a list of error messages found.
    - Performs lexing & parsing; returns syntax/lexer errors.
    - If parsing succeeds, runs the interpreter and returns runtime errors.
    - If no errors are found, returns an empty list.
    """
    errors = []

    # 1) Lexing & Parsing
    try:
        tokens = Lexer.lexer(code)
        parser = Parser.Parser(tokens)
        ast_tree = parser.parse_program()
    except SyntaxError as e:
        errors.append(f"SyntaxError: {e}")
        return errors
    except Exception as e:
        errors.append(f"Parser/Lexer Fatal Error: {e}")
        return errors

    # 2) Interpretation (runtime errors)
    interp = Evaluator.Interpreter()
    # capture stdout to avoid printing during analysis
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        interp.eval(ast_tree)
    except (NameError, ZeroDivisionError, TypeError) as e:
        # normalize message text
        msg = str(e)
        # drop any leading "Runtime Error: " if present
        if msg.startswith("Runtime Error: "):
            msg = msg[len("Runtime Error: "):]
        # classify common runtime errors
        if isinstance(e, NameError):
            errors.append(f"NameError: {msg}")
        elif isinstance(e, ZeroDivisionError):
            errors.append(f"ZeroDivisionError: {msg}")
        elif isinstance(e, TypeError):
            errors.append(f"TypeError: {msg}")
        else:
            errors.append(f"RuntimeError: {msg}")
    except Exception as e:
        errors.append(f"UnexpectedRuntimeError: {e}")
    finally:
        # always restore stdout
        sys.stdout = old_stdout

    return errors





