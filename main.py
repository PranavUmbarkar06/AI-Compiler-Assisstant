from Compiler import OfflineAssistant as off,OnlineAssistant as on
# -----------------------------------------------------------
import re 
import sys


def refine_code(code):
    new_code=''
    for i in code:
        if i in ['\n']:
            new_code+=' '
            continue
        new_code+=i
    return new_code


if __name__ == '__main__':


    code=open('main','r').read()
    code=refine_code(code)
    
    #ONLINE
    prompt_query = f"""
    Below is the complete Python code implementing a custom language compiler/interpreter, featuring a Lexer, Parser (Recursive Descent), and an Interpreter.

    The language supports:
    - Variable declaration (integer x = 10;)
    - Assignment (x = 20;)
    - Integer arithmetic (+, -, *, / with integer division)
    - Printing strings and expressions (print("Hello"); print(x + 1);)
    - Parentheses for precedence.

    Please analyze the provided code and give structured, actionable feedback focusing on the following areas:

    ---

    ## 1. Code Optimizations and Performance Suggestions 🚀
    Identify specific lines or components in the Lexer, Parser, or Interpreter that could be refactored for better performance or Pythonic clarity.
    - **Lexer:** Are the regex patterns efficient, or could the token definition order be improved?
    - **Interpreter:** Are there data structure changes that could speed up variable lookups (though the current global scope is simple)?

    ---

    ## 2. Robustness and Error Handling Suggestions 🛡️
    Point out potential runtime errors, type-checking issues, or logical flaws that the current implementation doesn't fully guard against.
    - **Type System:** The current language is only for integers. Suggest how to enforce the 'integer' type during **Assignment** to prevent bugs like `x = "hello";` if the parser was extended to allow un-declared string assignments.
    - **Ambiguity/Syntax:** Are there any cases where the grammar might lead to unexpected parsing (e.g., precedence issues, although arithmetic precedence seems correct)?
    - **Declaration/Redeclaration:** What happens if a user tries `integer x = 5; integer x = 10;`? Suggest a check to prevent this.

    ---

    ## 3. Feature Enhancements and Architecture Improvements ✨
    Suggest **three** logical, next-step features for this language and briefly describe the *minimum required changes* in each of the three components (Lexer, Parser, Interpreter) to implement them.

    1.  **Feature 1:** Conditional Statements (e.g., `if (x > 10) { ... }`)
    2.  **Feature 2:** String Concatenation (e.g., `print("Value: " + y);`)
    3.  **Feature 3:** Single-line Comments (e.g., `// This is a comment`)

    --- START OF CODE ---
    {code}
    --- End of Code
    """
    system_role = "Act as a professional compiler. Give nice helpful suggestions like a nice person."
    
    result = on.online_assistant(prompt_query, system_instruction=system_role)
    if result==False:
        analysis = off.offline_assistant(code)
        print("\n*** Analysis Report ***")
        for suggestion in analysis['suggestions']:
            print(suggestion)
        print("\n*** Runtime Output ***")
        print(analysis['runtime_output'])
        print('\n*** Final Symbol Table ***')
        print(analysis['final_state'])
    else:
    #OFFLINE
        print(result)
    