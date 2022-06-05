from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from setup import *

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
  app.run('127.0.0.1', 5600, debug=True)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
  file = request.files['file']
  file.save('./input/' + file.filename)
  path = './input/' + file.filename
  
  return {
    'status': 'success',
    'filename': file.filename
  }

@app.route('/getResponse', methods=['POST', 'GET'])
def get_response():
  import requests
  filename = request.args.get('filename')
  path = './input/' + filename
  print(path)
  response = detect_handwritten_ocr(path)
  results = display_detected_handwritten(path, response, filename)
  return {
    'filename': filename,
    'results': results
  }

@app.route('/output/<path:filename>', methods=['POST', 'GET'])
def output(filename):
  return send_from_directory("output", filename)