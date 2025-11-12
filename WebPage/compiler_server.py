from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import webbrowser

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/run', methods=['POST'])
def run_code():
    try:
        data = request.get_json()
        code = data.get('code', '')

        # Absolute path to your project root (where main.py and test.txt are)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        test_file_path = os.path.join(project_root, 'test.txt')

        # 1️⃣ Write the code directly into test.txt (next to main.py)
        with open(test_file_path, 'w', encoding='utf-8') as file:
            file.write(code)

        # 2️⃣ Run main.py as if you ran it manually in that folder
        result = subprocess.run(
            ['python', 'main.py'],
            cwd=project_root,       # 👈 set working directory
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        # Combine both outputs nicely
        return jsonify({
            "output": output,
            "error": error
        })

    except Exception as e:
        return jsonify({"output": "", "error": str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000...")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
