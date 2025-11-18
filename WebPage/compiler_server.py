import sys
import subprocess
import os

def install_requirements():
    base_dir = os.path.dirname(os.path.abspath(__file__))   # WebPage/
    req_path = os.path.join(base_dir, "..", "requirements.txt")  # one folder up

    req_path = os.path.abspath(req_path)  # normalize
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])

install_requirements()
# compiler_server.py (only the updated run_code route shown)
from flask import Flask, request, jsonify, send_from_directory
import os, webbrowser
import subprocess



# Ensure parent dir is importable (if required)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import main

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/run', methods=['POST'])
def run_code():
    try:
        data = request.get_json(force=True, silent=True)
        code = data.get('code', '') if data else ''
        if not code or not code.strip():
            return jsonify({"output": "", "error": "No code provided"}), 400

        # Call main.main(code) which now returns a structured dict
        result = main.main(code)

        # If code ran successfully, return stdout and symbols
        if result.get("ran"):
            run_result = result["run_result"]
            return jsonify({
                "output": run_result.get("stdout", ""),
                "symbols": run_result.get("symbols"),
                "error": ""
            }), 200
        else:
            # Fallback: assistant feedback available
            return jsonify({
                "output": result["run_result"].get("stdout", ""),
                "symbols": None,
                "error": result["run_result"].get("error", ""),
                "assistant": result.get("assistant")
            }), 200

    except Exception as e:
        return jsonify({"output": "", "error": str(e)}), 500


if __name__ == '__main__':
    print(r"Starting Flask server on http://127.0.0.1:5000...")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
