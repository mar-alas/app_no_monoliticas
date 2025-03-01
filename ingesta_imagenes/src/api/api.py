from src.aplicacion.servicio_ingesta_imagen import ServicioIngestaImagen
from io import BytesIO
from flask import Flask, jsonify, request, send_file
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from datetime import datetime
from uuid import uuid4

from src.seedwork.aplicacion.autenticacion import token_required
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
@token_required
def home():
    return jsonify(message="Welcome to the Flask app!")

@app.route('/ingesta-imagen', methods=['POST'])
@token_required
def ingesta_imagen():
    try:
        logger.info(f"Recibiendo imagen para procesar")
        if not ImagenDeAnonimizacionEsValida(request.files['image']).es_valido():
            return jsonify(error="La imagen de anonimizacion no es valida"), 400

        file = request.files['image']
        
        image_data = file.read()

        if not TamanioDeImagenEsValido(len(image_data)).es_valido():
            return jsonify(error="El tamaño de la imagen no es valido"), 400

        if not NombreDeImagenNoPuedeSerVacio(file.filename).es_valido():
            return jsonify(error="El nombre de la imagen no puede ser vacio"), 400
        
        if not FormatoDeImagenEsValido(file.filename).es_valido():
            return jsonify(error="Invalid file type, only .jpg, .png, jpeg allowed"), 400

        image_stream = BytesIO(image_data)
        proveedor = request.form['proveedor']
        logger.info(f"Imagen recibida de proveedor {proveedor}")
        servicio = ServicioIngestaImagen()
        servicio.procesar_y_enviar(nombre=file.filename, datos=image_stream, proveedor=proveedor, size=len(image_data))

        return jsonify(mensaje="Imagen enviada para procesamiento",), 200
    except Exception as e:
        return jsonify(error=f"Error inesperado: {str(e)}. Intente mas tarde.",), 500
    
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)