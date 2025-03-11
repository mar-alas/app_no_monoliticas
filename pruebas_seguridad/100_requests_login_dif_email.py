import requests
import json
import random
import string
import os
from faker import Faker

bff_ip = os.environ['BFF_IP'] = 'localhost'
url = f'http://{bff_ip}:8001/bff/login'
headers = {
    'Content-Type': 'application/json',
    'x-browser': 'chrome',
    'x-country': 'CO',
    'x-forwarded-for': '123.456.789.000',
    'x-os': 'windows'
}
email = "admin@saludtech.com"
fake = Faker()

def make_request(email, password):
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

def main():
    N = 100
    for _ in range(N):
        password = fake.password()
        response = make_request(email, password)
        response_message = json.loads(response.text)
        with open('pruebas_seguridad/100_requests_diff_pass.csv', 'a') as f:
            f.write(f"{response.status_code},{response_message['message']},{email},{password}\n")
        if 'token' in response.text:
            print(f"ERROR: Se logro obtener el token: {response.text}")
        else:
            print(f"Se genero un error de credenciales invalidas como se esperaba. Response: {response.text}")

if __name__ == "__main__":
    main()