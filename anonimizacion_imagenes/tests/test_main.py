import pytest
from src.api.api import app
from werkzeug.datastructures import FileStorage
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secreto_super_seguro"

def generate_token(user_id: str):
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client



def test_home_route(client):
    token=generate_token("test_user")
    response = client.get('/', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    

