from flask import Flask, request, jsonify, send_from_directory
import os, sys, webbrowser

# Add the parent folder (project root) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your compiler main file directly
import main

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/run', methods=['POST'])
def run_code():
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        if not code:
            return jsonify({"output": "", "error": "No code provided"})

        # Call main.py function directly (no test.txt)
        result_output = main.run_compiler_from_code(code)
        return jsonify({"output": result_output, "error": ""})

    except Exception as e:
        return jsonify({"output": "", "error": str(e)})


if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000...")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
