#this runs with python3 src/api/api.py from microservice root folder

from io import BytesIO
from flask import Flask, jsonify, request, send_file
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen

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

    if file and file.filename.endswith('.jpeg'):
        image_data = file.read()
        image_stream = BytesIO(image_data)
        image_stream2=servicio_anonimizar_imagen(image_stream)
        return send_file(
            image_stream2,
            mimetype="image/jpeg",  # Correct MIME type for JPEG images
            as_attachment=False,    # Set to True if you want to force download
            download_name=file.filename  # Optional: Set the filename for the response
        )
    else:
        return jsonify(error="Invalid file type, only .jpg allowed"), 400

if __name__ == '__main__':
    app.run(debug=True)


