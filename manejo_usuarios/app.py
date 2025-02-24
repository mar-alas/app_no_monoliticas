import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from flask import Flask
from api.auth import auth_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix="/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
