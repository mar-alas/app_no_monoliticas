from functools import wraps
from flask import Flask, jsonify, request
from src.seedwork.aplicacion.autenticacion import token_required
from src.infraestructura.respositorios import RepositorioImagenesAnonimizadasSQLAlchemy
from seedwork.dominio.security_rules import PaisNoPermitido, NavegadorNoPermitido, SistemaOperativoNoPermitido, DominioCorreoNoPermitido, IPNoPermitida

app = Flask(__name__)

# Middleware para validar reglas de seguridad
def validar_reglas_de_seguridad(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        country = request.headers.get("X-Country", "").upper()
        browser = request.headers.get("X-Browser", "").lower()
        os = request.headers.get("X-OS", "").lower()
        ip_address = request.headers.get("X-Forwarded-For", "")

        reglas = [
            PaisNoPermitido(country),
            NavegadorNoPermitido(browser),
            SistemaOperativoNoPermitido(os)
            # IPNoPermitida(ip_address)
        ]

        for regla in reglas:
            if not regla.es_valido():
                return jsonify({"message": "No autorizado", "reason": regla.mensaje_error()}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return jsonify(message="Bienvenido a anonimizacion de imagenes!")


@app.route('/anonimizacion/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/anonimizacion/imagenes', methods=['GET'])
@token_required
@validar_reglas_de_seguridad
def consulta():
    repositorio = RepositorioImagenesAnonimizadasSQLAlchemy()
    imagenes = repositorio.obtener_inventario_imagenes_anonimizadas()
    return jsonify(imagenes),200
