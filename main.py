# main.py
import sys
import traceback
from io import StringIO

# Try to import Compiler modules (adjust path elsewhere if needed)
try:
    from Compiler import OnlineAssistant as on, OfflineAssistant as off, Lexer, Parser, Evaluator
except Exception:
    # if running from project root and Compiler is sibling, try relative import fallback
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    compiler_dir = os.path.join(current_dir, "Compiler")
    if compiler_dir not in sys.path:
        sys.path.insert(0, compiler_dir)
    from Compiler import OnlineAssistant as on, OfflineAssistant as off, Lexer, Parser, Evaluator


def run_compiler_from_code(code: str):
    
    system_instruction = r'''
    You are a friendly, homely compiler assistant who reviews user code to find syntax, logical, and runtime errors.
    You point out exact lines and explain issues clearly yet warmly.
    Use plain, comforting language, not robotic tone.
    Return results in structured form: Errors, Explanation, Fix, Optimization, Corrected Code.
    Always provide corrected code snippets. If code has no issues, say so and suggest small improvements.
    Keep responses under 200 words. Focus on clarity, correctness, and empathy.
    Let the corrected code be raw text with \n and not marked down.
    
    This is the grammar of the language:
    PROGRAM     → STMT_LIST EOF
    STMT_LIST   → (STMT)*
    STMT        → DECL | ASSIGN | PRINT_STMT
    DECL        → "integer" ID "=" EXPR ";" 
    ASSIGN      → ID "=" EXPR ";"
    PRINT_STMT  → "print" "(" EXPR ")" ";"
    EXPR        → TERM { ("+" | "-") TERM }
    TERM        → FACTOR { ("*" | "/") FACTOR }
    FACTOR      → NUMBER | STRING | ID | "(" EXPR ")"
    NUMBER      → DIGIT+
    STRING      → '"' CHAR* '"'
    ID          → LETTER (LETTER | DIGIT | "_")*
    LETTER      → [a-zA-Z_]
    DIGIT       → [0-9]
    
    
    
    ''' 
    try:

        response = on.online_assistant(prompt=code, system_instruction=system_instruction)
    except Exception:
        response = None

    if not response:
        response = off.offline_assistant(code)

    return {
        "assistant_type": "online" if response is not None and response is not off.offline_assistant.__name__ else "offline",
        "assistant": response
    }


def run(code: str, show_tokens: bool = False) -> dict:
    """
    Execute code through Lexer->Parser->Evaluator.
    Returns a dict:
      {
        "success": bool,
        "stdout": "<captured stdout>",
        "symbols": { ... final symbol table ... } or None,
        "error": "<error text>" or "",
      }
    """
    if code is None:
        return {"success": False, "stdout": "", "symbols": None, "error": "No code provided."}

    old_stdout = sys.stdout
    buffer = StringIO()
    sys.stdout = buffer

    try:
        # LEXER
        tokens = Lexer.lexer(code)

        if show_tokens:
            print("TOKENS:")
            for t in tokens:
                print(" ", t)
            print()

        # PARSER
        parser = Parser.Parser(tokens)
        ast = parser.parse_program()

        # INTERPRETER
        interp = Evaluator.Interpreter()
        interp.eval(ast)

        
        print()
        print(interp)

        sys.stdout.flush()
        output = buffer.getvalue()

        return {"success": True, "stdout": output, "symbols": interp.symbol_table, "error": ""}

    except Exception as e:
        # restore stdout before returning
        sys.stdout = old_stdout
        tb = traceback.format_exc()
        return {"success": False, "stdout": buffer.getvalue(), "symbols": None, "error": f"{type(e).__name__}: {e}\n{tb}"}
    finally:
        sys.stdout = old_stdout


def main(code: str):
    
    try:
        result = run(code, show_tokens=False)
        # If interpreter raised an error (success False), fallback to assistant
        if not result.get("success"):
            assistant_result = run_compiler_from_code(code)
            return {"ran": False, "run_result": result, "assistant": assistant_result}
        else:
            return {"ran": True, "run_result": result, "assistant": None}
    except Exception as e:
        # Unexpected top-level error: return assistant fallback
        assistant_result = run_compiler_from_code(code)
        return {"ran": False, "run_result": {"success": False, "stdout": "", "symbols": None, "error": str(e)}, "assistant": assistant_result}



