from flask import Flask, jsonify
from src.seedwork.aplicacion.autenticacion import token_required

app = Flask(__name__)

@app.route('/')
@token_required
def home():
    return jsonify(message="Bienvenido a anonimizacion de imagenes!")

    


