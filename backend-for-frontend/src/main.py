from flask import Flask
from api.v1.web_controller import web_bp
from api.v1.mobile_controller import mobile_bp

def create_app():
    app = Flask(__name__)
    
    # Web routes
    app.register_blueprint(web_bp, url_prefix='/bff/web')

    # mobile routes
    app.register_blueprint(mobile_bp, url_prefix='/bff/mobile')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=3001)
