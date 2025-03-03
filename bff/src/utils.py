import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'
ANONIMIZACION_SERVICE_URL: str = os.getenv("ANONIMIZACION_SERVICE_URL", "http://anonimizacion_service:5001")

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")

def consultar_schema_registry(topico: str) -> dict:
    try:
        json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
        return json.loads(json_registry.get('data',{}))
    except requests.exceptions.ConnectionError:
        print(f"No se pudo conectar al broker Pulsar en {broker_host()}:8080")
        # Devolver un esquema vacío o un esquema de fallback
        return {"type": "record", "name": "DefaultSchema", "fields": []}

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)

def obtener_imagenes_anonimizadas():
    url = f"{ANONIMIZACION_SERVICE_URL}/anonimizacion/imagenes"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error en la respuesta: {response.status_code}")

        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"Error de conexión: {e}")
        print(f"URL: {url}")