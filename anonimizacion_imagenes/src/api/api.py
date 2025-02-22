#this runs with python3 src/api/api.py from microservice root folder
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask app!")

@app.route('/anonimizar-imagen', methods=['POST'])
def anonimizar_imagen():
    if 'image' not in request.files:
        return jsonify(error="No image part"), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file and file.filename.endswith('.jpg'):
        # Process the image here
        return jsonify(message="Image received and processed"), 200
    else:
        return jsonify(error="Invalid file type, only .jpg allowed"), 400


if __name__ == '__main__':
    app.run(debug=True)


