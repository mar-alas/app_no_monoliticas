from flask import Blueprint, request, jsonify
from aplicacion.authentication_service import AuthenticationService
from aplicacion.token_service import TokenService
from infraestructura.sql_user_repository import SQLUserRepository
from infraestructura.db import get_db
from functools import wraps

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

@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    user = auth_service.register_user(data["name"], data["email"], data["password"])
    return jsonify({
        "message": "Usuario registrado exitosamente",
        "user_id": str(user.id)
    }), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    ...

@auth_blueprint.route("/profile", methods=["GET"])
@token_required
def profile(user_id):
   ...
