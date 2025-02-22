import pytest
from src.api.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'message' in json_data
    assert json_data['message'] == 'Welcome to the Flask app!'

def test_anonimizar_route(client):
    # Prepare a test image file
    test_image_path = "tests/test_image.jpg"
    with open(test_image_path, "wb") as f:
        f.write(b"fake image data")  # Create a dummy image file

    with open(test_image_path, "rb") as image_file:
        response = client.post(
            "/anonimizar-imagen",
            data={"image": image_file, "description": "Test image"},
            content_type="multipart/form-data",
        )

    assert response.status_code == 200
    json_data = response.get_json()
    assert 'Image received and processed' == json_data['message']
