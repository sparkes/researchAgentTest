from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# API service URL (will be set to the Docker service name)
API_URL = 'http://api:5000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze/upload', methods=['POST'])
def analyze_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Forward the file to the API service
    files = {'file': (file.filename, file.stream, file.content_type)}
    response = requests.post(f'{API_URL}/analyze/upload', files=files)
    return response.json(), response.status_code

@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Forward the URL to the API service
    response = requests.post(f'{API_URL}/analyze/url', json=data)
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
