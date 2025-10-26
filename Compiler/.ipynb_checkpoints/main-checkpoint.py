from Lexer import lexer
from Parser import Parser
from Evaluator import Interpreter
from ai_assistant import HybridAIAssistant

def main():
    print("====== Mini-C Compiler with AI Assistant ======\n")
    assistant = HybridAIAssistant()

    while True:
        print("\nEnter your code line by line (type 'exit' to finish input):")
        code_lines = []
        while True:
            line = input()
            if line.strip().lower() == "exit":
                break
            code_lines.append(line)

        if not code_lines:
            print("No code entered. Exiting...")
            break

        code = "\n".join(code_lines)

        #AI suggests fixes or auto-correction before running
        code = assistant.suggest_and_autocorrect(code)

        try:
            #Lexer
            tokens = lexer(code)

            #Parser
            parser = Parser(tokens)
            tree = parser.parse_program()

            #Interpreter
            interp = Interpreter()
            interp.eval(tree)

            #Offline AI optimization hints
            if not assistant.online:
                print("\nOptimization hints (offline AI only):")
                if "* 1" in code or "+ 0" in code:
                    print("Hint: You can remove '*1' or '+0' as they are unnecessary.")
                if re.search(r'(\w+)\s*=\s*\1\s*;', code):
                    print("Hint: Assigning a variable to itself is redundant.")

        except Exception as e:
            assistant.handle_error(str(e))

        cont = input("\nDo you want to enter more code? (y/n): ").strip().lower()
        if cont != "y":
            print("Exiting compiler. Goodbye!")
            break

if __name__ == "__main__":
    main()
