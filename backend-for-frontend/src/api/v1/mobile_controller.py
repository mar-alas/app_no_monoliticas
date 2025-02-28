from flask import Blueprint, jsonify
import uuid
from services.ping_service import do_ping

mobile_bp = Blueprint('mobile_bp', __name__)

@mobile_bp.route('/v1/ping', methods=['GET'])
def ping():
    data = {
        "client": "mobile",
        "data": {
            "status": do_ping()
        }
    }
    response = jsonify(data)
    response.headers['X-frontend'] = 'MOBILE'
    response.headers['X-backend'] = 'MOBILE'
    response.headers['X-backend-version'] = 'v1'
    response.headers['X-trace-id'] = str("mobile_bff_")+str(uuid.uuid4())
    return response
