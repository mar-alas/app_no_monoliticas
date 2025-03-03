from flask import Flask, jsonify
from src.seedwork.aplicacion.autenticacion import token_required
from src.infraestructura.respositorios import RepositorioImagenesAnonimizadasSQLAlchemy
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Bienvenido a anonimizacion de imagenes!")


@app.route('/anonimizacion/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/anonimizacion/imagenes', methods=['GET'])
def consulta():
    repositorio=RepositorioImagenesAnonimizadasSQLAlchemy()
    imagenes = repositorio.obtener_inventario_imagenes_anonimizadas()
    return jsonify(imagenes),200
