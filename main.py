# main.py

import sys
import os
import re

# Adjust the path to find the Compiler module (assuming Compiler is a subdirectory)
# You may need to adjust this depending on your exact structure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Assuming your modules are in Compiler/
from Compiler.OnlineAssistant import online_assistant as on

# --- MOCK OF OFFLINE COMPILER ASSISTANT ---
def offline_assistant(code: str):
    """Mocks a compiler run based on the new test.txt flaws."""
    
    # Check for the two missing semicolons from the fixed test.txt file
    if 'integer width = 5;' in code and 'area = length * width;' in code:
        # Success case (the code has the semicolon fixes)
        return {
            'status': 'OK',
            'suggestions': [],
            'runtime_output': 'Result: 50\n' # Expected output of the logic
        }
    else:
        # Failure case (the original code is missing semicolons or has other errors)
        errors = []
        if '#' in code and 'SKIP' not in code: # Simple mock to catch the unhandled # from the old scenario
             # This error should now be caught by the real lexer.py!
             pass 

        if 'integer width = 5' in code and ';' not in code.split('\n')[2]:
             errors.append("Line 3: Missing SEMICOLON (';') after declaration of 'width'")
        if 'area = length * width' in code and ';' not in code.split('\n')[5]:
             errors.append("Line 6: Missing SEMICOLON (';') after assignment to 'area'")

        if not errors and 'print' in code: # If no major errors but still can't compile (like the initial case)
             errors.append("SYNTAX_ERROR: Lexing was successful, but the parser failed due to a missing terminal.")

        return {
            'status': 'SYNTAX_ERROR',
            'suggestions': errors if errors else ["General Parser Failure: Check for missing semicolons or undeclared variables."],
            'runtime_output': ''
        }
# --- END MOCK ---


# Define the input file name
CODE_FILE = 'test.txt'

def extract_code_block(text: str) -> str | None:
    """Extracts the first code block (```...```) from a string."""
    match = re.search(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def display_success(file_name, runtime_output):
    """Displays the concise success message and output."""
    print("=========================================")
    print(f"✅ FILE RUNNING FINE: '{file_name}'")
    print("--- OUTPUT ---")
    print(runtime_output if runtime_output else "No output printed.")
    print("=========================================")

def run_compiler_assistant():
    """Reads code, runs offline analysis, and uses online assistant for fixes on failure."""
    
    # 1. Read the source code file
    try:
        with open(CODE_FILE, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: Source code file '{CODE_FILE}' not found. Create it with the sample code.")
        sys.exit(1)
        
    if not code.strip():
        print(f"Code file '{CODE_FILE}' is empty. Nothing to analyze.")
        return

    # --- 1. OFFLINE ANALYSIS ---
    analysis = offline_assistant(code)
    status = analysis.get('status', 'UNKNOWN_ERROR')
    suggestions = analysis.get('suggestions', [])
    runtime_output = analysis.get('runtime_output', '')

    if status == 'OK':
        # --- SUCCESS CASE: DIRECT OUTPUT ---
        display_success(CODE_FILE, runtime_output)
        
    else:
        # --- FAILURE CASE: INVOKE ONLINE ASSISTANT FOR FIX ---
        
        # 🎯 Print the original error clearly
        print("=========================================")
        print(f"❌ ERROR DETECTED in '{CODE_FILE}' (Status: {status})")
        print("--- Original Compiler Diagnostics ---")
        for suggestion in suggestions:
            print(f"  {suggestion}")
        
        print("\n--- Attempting AI Fix (Gemini Assistant) ---")
        
        # 🎯 FIX: EXTREMELY specific system role to prevent over-fixing
        system_role = (
            "You are an expert compiler error assistant. Your ONLY job is to fix the "
            "provided source code based ONLY on the compiler diagnostics. "
            "You MUST preserve all working code and ONLY modify lines necessary to resolve the syntax error (e.g., adding a missing semicolon). "
            "You MUST adhere strictly to the original programming style. "
            "You MUST return the **FULL, CORRECTED SOURCE CODE** in a single "
            "triple backtick code block, and NOTHING else. Do not provide an explanation."
        )
        
        error_message = "\n".join(suggestions)
        prompt_query = (
            f"Compiler Diagnostics:\n{error_message}\n\n"
            f"Original Code to FIX:\n```\n{code}\n```\n\n"
            f"TASK: Provide the complete, corrected source code in a single code block."
        )
        
        ai_response = on(prompt_query, system_instruction=system_role)
        
        if ai_response:
            
            # --- EXTRACT AND RERUN ---
            fixed_code = extract_code_block(ai_response)
            
            if fixed_code:
                print("\n--- Fix Extracted. Rerunning Code... ---")
                
                # Rerun the compiler with the AI-suggested fixed code
                rerun_analysis = offline_assistant(fixed_code)
                rerun_status = rerun_analysis.get('status')
                
                if rerun_status == 'OK':
                    # --- FINAL SUCCESS CASE ---
                    print("✅ FIX SUCCESSFUL. The corrected code is:")
                    print("```")
                    print(fixed_code)
                    print("```")
                    display_success("AI-Fixed Code", rerun_analysis.get('runtime_output', ''))
                else:
                    print(f"\n[Rerun Failed] The AI-suggested fix did not resolve the error (Status: {rerun_status}).")
                    print("New Diagnostics:")
                    for suggestion in rerun_analysis.get('suggestions', []):
                         print(f"  {suggestion}")
            else:
                print("\n[AI Fix Failed] Could not extract a valid code block from the AI's response.")
                # You might print the raw AI response here for manual debugging
                # print(f"AI Output: {ai_response}") 
        else:
            print("\n[AI Fix Failed] Could not connect to or retrieve a fix from the Online Assistant.")


def run_compiler_from_code(code: str):
    """Runs the compiler assistant using a direct code string instead of test.txt."""
    analysis = offline_assistant(code)
    status = analysis.get('status', 'UNKNOWN_ERROR')
    suggestions = analysis.get('suggestions', [])
    runtime_output = analysis.get('runtime_output', '')

    if status == 'OK':
        # --- SUCCESS CASE ---
        output = []
        output.append("=========================================")
        output.append("✅ FILE RUNNING FINE (from memory input)")
        output.append("--- OUTPUT ---")
        output.append(runtime_output if runtime_output else "No output printed.")
        output.append("=========================================")
        return "\n".join(output)

    else:
        # --- FAILURE CASE ---
        output = []
        output.append("=========================================")
        output.append(f"❌ ERROR DETECTED (Status: {status})")
        output.append("--- Original Compiler Diagnostics ---")
        for suggestion in suggestions:
            output.append(f"  {suggestion}")

        output.append("\n--- Attempting AI Fix (Gemini Assistant) ---")

        # System role and AI request (same as your original)
        system_role = (
            "You are an expert compiler error assistant. Your ONLY job is to fix the "
            "provided source code based ONLY on the compiler diagnostics. "
            "You MUST preserve all working code and ONLY modify lines necessary to resolve the syntax error. "
            "Return the FULL, CORRECTED SOURCE CODE in a single triple backtick code block, nothing else."
        )

        error_message = "\n".join(suggestions)
        prompt_query = (
            f"Compiler Diagnostics:\n{error_message}\n\n"
            f"Original Code to FIX:\n```\n{code}\n```\n\n"
            f"TASK: Provide the complete, corrected source code in a single code block."
        )

        ai_response = on(prompt_query, system_instruction=system_role)
        fixed_code = extract_code_block(ai_response) if ai_response else None

        if fixed_code:
            rerun_analysis = offline_assistant(fixed_code)
            if rerun_analysis.get('status') == 'OK':
                output.append("\n✅ FIX SUCCESSFUL. The corrected code is:")
                output.append("```")
                output.append(fixed_code)
                output.append("```")
                output.append("-----------------------------------------")
                output.append("Re-run Output:")
                output.append(rerun_analysis.get('runtime_output', ''))
                output.append("=========================================")
            else:
                output.append(f"\n[Rerun Failed] Status: {rerun_analysis.get('status')}")
        else:
            output.append("\n[AI Fix Failed] Could not extract or get a valid fix.")
        return "\n".join(output)



if __name__ == '__main__':
    run_compiler_assistant()