from flask import Blueprint, jsonify

app = Blueprint('verificacion_api', __name__)

@app.route('/')
def home():
    return jsonify(message="Microservicio de verificación de anonimización")

@app.route('/verificacion/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/verificacion/estado', methods=['GET'])
def estado():
    return jsonify({
        "servicio": "verificacion_anonimizacion",
        "estado": "activo",
        "version": "1.0.0"
    }), 200