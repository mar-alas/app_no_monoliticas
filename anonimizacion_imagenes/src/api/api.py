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

    


