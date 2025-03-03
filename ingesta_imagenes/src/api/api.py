from src.config.db import init_db
from src.aplicacion.servicio_ingesta_imagen import ServicioIngestaImagen
from io import BytesIO
from flask import Flask, jsonify, request, send_file
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from datetime import datetime
from uuid import uuid4
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

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

@app.route('/ingesta-imagen/ping', methods=['GET'])
def ping():
    return jsonify(message="pong"), 200



if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///../src/infraestructura/ingesta.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'

    from src.config.db import init_db
    db = init_db(app)
    
    # Import the model after db is initialized
    from src.infraestructura.dto import IngestaImagenes
    
    # Create all tables
    with app.app_context():
        db.create_all()
        
    app.run(host="0.0.0.0", port=5000, debug=True)