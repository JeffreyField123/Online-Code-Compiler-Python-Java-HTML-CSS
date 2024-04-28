from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid
import time
import psutil

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from your HTML pages


def measure_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 2)  # Convert bytes to MB


@app.route('/compile_code', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data['code']
    language = data['language']

    filename = f"{uuid.uuid4()}"
    if language == 'python':
        filename += '.py'
        with open(filename, 'w') as file:
            file.write(code)
        run_command = ['python', filename]
    elif language == 'javascript':
        filename += '.js'
        with open(filename, 'w') as file:
            file.write(code)
        run_command = ['node', filename]
    else:
        return jsonify(output='', error='Unsupported language')

    try:
        start_time = time.time()
        memory_before = measure_memory_usage()
        output = subprocess.run(run_command, capture_output=True, text=True, timeout=30)
        end_time = time.time()
        execution_time = end_time - start_time
        memory_after = measure_memory_usage()
        memory_used = memory_after - memory_before

        if output.stderr:
            return jsonify(output='', error=output.stderr, time=execution_time, memory=memory_used)
        return jsonify(output=output.stdout, error='', time=execution_time, memory=memory_used)
    finally:
        os.remove(filename)


@app.route('/translate_code', methods=['POST'])
def translate_code():
    data = request.get_json()
    code = data['code']
    source_language = data['source_language']
    target_language = data['target_language']

    # Simulated translation (this should be replaced with actual logic or an API)
    if source_language == 'python' and target_language == 'javascript':
        translated_code = code.replace('print', 'console.log')
    elif source_language == 'javascript' and target_language == 'python':
        translated_code = code.replace('console.log', 'print')
    else:
        return jsonify(translated_code='', error='Translation not supported between selected languages')

    return jsonify(translated_code=translated_code, error='')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

