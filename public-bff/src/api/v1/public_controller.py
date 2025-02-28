from flask import Blueprint, jsonify
import uuid
from services.ping_service import do_ping

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/v1/ping', methods=['GET'])
def ping():
    data = {
        "client": "public",
        "data": {
            "status": do_ping()
        }
    }
    response = jsonify(data)
    response.headers['X-frontend'] = 'any'
    response.headers['X-backend'] = 'public'
    response.headers['X-backend-version'] = 'v1'
    response.headers['X-trace-id'] = str("public_bff_")+str(uuid.uuid4())
    return response
