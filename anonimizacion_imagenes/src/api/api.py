from flask import Flask, jsonify
from src.seedwork.aplicacion.autenticacion import token_required

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Bienvenido a anonimizacion de imagenes!")


@app.route('/anonimizacion/ping', methods=['GET'])
def ping():
    return "pong", 200
