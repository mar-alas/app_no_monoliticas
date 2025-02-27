import jwt
from functools import wraps
from flask import request, jsonify

# TODO: poner secret key en variable de entorno
SECRET_KEY = "secreto_super_seguro"  # misma clave que en manejo_usuarios

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = payload["sub"]
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(*args, **kwargs)
    return decorated