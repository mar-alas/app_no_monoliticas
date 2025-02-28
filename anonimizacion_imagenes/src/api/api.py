#this runs with python3 src/api/api.py from microservice root folder
import os
from io import BytesIO
from flask import Flask, jsonify, request, send_file
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen
from src.infraestructura.publicadores import PublicadorEventos
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from src.seedwork.aplicacion.autenticacion import token_required
from src.seedwork.infraestructura.utils import broker_host

app = Flask(__name__)

@app.route('/')
@token_required
def home():
    return jsonify(message="Welcome to the Flask app!")

#TODO quitar ruta
@app.route('/anonimizar-imagen', methods=['POST'])
@token_required
def anonimizar_imagen():
    try:

        file = request.files['image']
        
        image_data = file.read()
        
        image_stream_img_sin_anonimizar = BytesIO(image_data)

        servicio_anonimizar_imagen(file.filename,image_stream_img_sin_anonimizar)
        
        return jsonify(message="Imagen anonimizada correctamente"), 200
    
    except Exception as e:
        return jsonify(error=f"Error inesperado: {str(e)}. Intente mas tarde.",), 500
    


