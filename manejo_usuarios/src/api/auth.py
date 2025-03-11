from flask import Blueprint, request, jsonify
from aplicacion.authentication_service import AuthenticationService
from aplicacion.token_service import TokenService
from infraestructura.sql_user_repository import SQLUserRepository
from infraestructura.db import get_db
from functools import wraps
from dominio.security_rules import PaisNoPermitido, NavegadorNoPermitido, SistemaOperativoNoPermitido, DominioCorreoNoPermitido, IPNoPermitida

auth_blueprint = Blueprint("auth", __name__)

db = next(get_db())
user_repo = SQLUserRepository(db)
auth_service = AuthenticationService(user_repo)

# Middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"message": "Token es requerido"}), 401

        token = token.split(" ")[1]
        user_id = TokenService.verify_token(token)
        if not user_id:
            return jsonify({"message": "Token inválido o expirado"}), 401

        return f(user_id, *args, **kwargs)
    return decorated

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
            SistemaOperativoNoPermitido(os),
            IPNoPermitida(ip_address)
        ]

        for regla in reglas:
            if not regla.es_valido():
                return jsonify({"message": "No autorizado", "reason": regla.mensaje_error()}), 401

        return f(*args, **kwargs)
    return decorated



@auth_blueprint.route("/register", methods=["POST"])
@validar_reglas_de_seguridad
def register():
    data = request.json

    if not DominioCorreoNoPermitido(data["email"]).es_valido():
        return jsonify({"message": "No autorizado: dominio de correo no permitido"}), 401

    try:
        result = auth_service.register_user(data["name"], data["email"], data["password"])
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_blueprint.route("/login", methods=["POST"])
@validar_reglas_de_seguridad
def login():
    data = request.json

    if not DominioCorreoNoPermitido(data["email"]).es_valido():
        return jsonify({"message": "No autorizado: dominio de correo no permitido"}), 401

    user = auth_service.authenticate_user(data["email"], data["password"])
    if not user:
        return jsonify({"message": "Credenciales inválidas"}), 401

    token = TokenService.generate_token(user.id)
    return jsonify({
        "message": "Autenticación exitosa",
        "token": token
    })

@auth_blueprint.route("/ping", methods=["GET"])
def ping():
        return jsonify({"message": "pong"})

@auth_blueprint.route("/profile", methods=["GET"])
@token_required
@validar_reglas_de_seguridad
def profile(user_id):
    return jsonify({"message": "Perfil de usuario", "user_id": user_id})
