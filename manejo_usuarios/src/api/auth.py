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
    ...

@auth_blueprint.route("/register", methods=["POST"])
def register():
    ...

@auth_blueprint.route("/login", methods=["POST"])
def login():
    ...

@auth_blueprint.route("/profile", methods=["GET"])
@token_required
def profile(user_id):
   ...
