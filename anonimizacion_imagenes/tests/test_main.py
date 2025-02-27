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
    json_data = response.get_json()
    assert 'message' in json_data
    assert json_data['message'] == 'Welcome to the Flask app!'

def test_anonimizar_route(client):
    token=generate_token("test_user")
    # Prepare a test image file
    test_image_path = "tests/test_image.jpeg"

    with open(test_image_path, "rb") as image_file:
        file_storage = FileStorage(
            stream=image_file,
            filename="test_image.jpeg",
            content_type="image/jpeg"
        )

        response = client.post(
            "/anonimizar-imagen",
            data={"image": file_storage, "description": "Test image"},
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    assert response.mimetype == "image/jpeg"
