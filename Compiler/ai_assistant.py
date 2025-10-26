import re
import socket

# Try to import OpenAI for online AI
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class OfflineAIAssistant:
    """
    Offline AI Assistant:
    -Explains errors
    -Suggests fixes
    -Auto-corrects code for:
    -Trailing operators
    -Missing semicolons
    -Print statements with expressions
    -Undeclared variables (auto-add 'integer')
    """

    def __init__(self):
        self.declared_vars = set()  # Track variables declared in this session

    def explain_error(self, error_msg):
        if "Unexpected charecter" in error_msg or "SyntaxError" in error_msg:
            return f"{error_msg}\nHint: Check for missing operators, extra symbols, or semicolons."
        elif "not declared" in error_msg or "NameError" in error_msg:
            return f"{error_msg}\nHint: Declare the variable first using 'integer var = value;'"
        else:
            return f"{error_msg}\nHint: Review your code for syntax mistakes."

    def suggest_fix(self, code):
        lines = code.split('\n')
        fixed_lines = []
        changes_made = False  # Track if any line actually changed

        for line in lines:
            original_line = line
            line = line.strip()
            if not line:
                fixed_lines.append(line)
                continue

            # Fix trailing operator
            if re.search(r'[+\-*/]\s*$', line):
                print("Suggestion: Incomplete arithmetic expression detected. Adding 0 to complete it.")
                line += '0'

            # Add semicolon if missing
            if not line.endswith(';'):
                print("Suggestion: Missing semicolon at end of statement. Adding it.")
                line += ';'

            # Fix print without parentheses
            print_match = re.match(r'^print\s+([a-zA-Z_]\w*)\s*;?', line)
            if print_match:
                varname = print_match.group(1)
                print("Suggestion: Print statement missing parentheses. Fixing it.")
                line = f"print({varname});"

            # Auto-declare undeclared variables
            assign_match = re.match(r'^([a-zA-Z_]\w*)\s*=', line)
            if assign_match:
                var = assign_match.group(1)
                if var not in self.declared_vars:
                    print(f"Suggestion: Variable '{var}' undeclared. Adding 'integer {var} ='.")
                    line = f"integer {line}"
                    self.declared_vars.add(var)

            # Check if line actually changed
            if line != original_line:
                changes_made = True

            fixed_lines.append(line)

        fixed_code = '\n'.join(fixed_lines)
        if changes_made:
            choice = input("Do you want me to auto-correct all suggested fixes? (y/n): ").strip().lower()
            if choice == 'y':
                print("Auto-corrected Code:\n", fixed_code)
                return fixed_code
        # No changes or user chose 'n'
        return code


class HybridAIAssistant:
    """
    Hybrid AI Assistant:
    - Uses ChatGPT API if online and key available
    - Falls back to offline AI otherwise
    """

    def __init__(self):
        self.online = self.check_internet()
        self.api_client = None
        if self.online and OpenAI is not None:
            try:
                self.api_client = OpenAI(api_key="AIzaSyDp5F0Fu0bpVjT57poMr-_pUlTA-YODouQ")  # <-- replace with your key
                print("Using Online ChatGPT-powered AI Assistant")
            except Exception:
                print("API key or connection issue. Falling back to offline AI.")
                self.online = False
        else:
            print("Using Offline Logic-based AI Assistant")
            self.online = False

        self.offline_ai = OfflineAIAssistant()

    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception:
            return False

    def handle_error(self, error_msg):
        if self.online and self.api_client:
            try:
                response = self.api_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"Explain this compiler error: {error_msg}"}]
                )
                print("ChatGPT says:", response.choices[0].message.content.strip())
            except Exception:
                print("API Error! Using Offline Explanation...")
                print(self.offline_ai.explain_error(error_msg))
        else:
            print(self.offline_ai.explain_error(error_msg))

    def suggest_and_autocorrect(self, code):
        if self.online and self.api_client:
            try:
                response = self.api_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": f"Check and suggest fixes or optimizations for this mini-C code:\n{code}"}
                    ]
                )
                suggestion = response.choices[0].message.content.strip()
                print("ChatGPT Suggestion:", suggestion)
            except Exception:
                print("API Error! Using Offline Logic...")
                code = self.offline_ai.suggest_fix(code)
        else:
            code = self.offline_ai.suggest_fix(code)

        return code
