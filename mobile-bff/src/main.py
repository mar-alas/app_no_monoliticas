from flask import Flask
from api.v1.mobile_controller import mobile_bp

def create_app():
    app = Flask(__name__)

    # mobile routes
    app.register_blueprint(mobile_bp, url_prefix='/bff/mobile')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=3003)
