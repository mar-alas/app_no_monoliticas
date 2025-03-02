from flask import Blueprint, jsonify
import uuid
from services.ping_service import do_ping

web_bp = Blueprint('web_bp', __name__)

@web_bp.route('/v1/ping', methods=['GET'])
def ping():
    data = {
        "client": "web",
        "data": {
            "status": do_ping()
        }
    }
    response = jsonify(data)
    response.headers['X-frontend'] = 'WEB'
    response.headers['X-backend'] = 'WEB'
    response.headers['X-backend-version'] = 'v1'
    response.headers['X-trace-id'] = str("web_bff_")+str(uuid.uuid4())
    return response
