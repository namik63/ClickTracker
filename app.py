from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DATA_FILE = "sneakers.xlsx"

# Ensure Excel file exists with correct headers
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["timestamp", "ip", "user_agent"])
    df.to_excel(DATA_FILE, index=False)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/log_visit', methods=['POST'])
def log_visit():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'Unknown')

        new_data = pd.DataFrame([{
            "timestamp": timestamp,
            "ip": ip,
            "user_agent": user_agent
        }])

        existing_data = pd.read_excel(DATA_FILE)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        combined_data.to_excel(DATA_FILE, index=False)

        return jsonify({"message": "Visit logged"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5020, debug=True)
