from google.cloud import storage
import logging
import os
from io import BytesIO

import warnings
warnings.filterwarnings("ignore", message="As the c extension couldn't be imported, `google-crc32c` is using a pure python implementation that is significantly slower.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'your_key_file.json'
credentials_file = ".keys/appnomonoliticas.json"

class GCPStorage:
    def __init__(self):
        self.cliente = storage.Client.from_service_account_json(credentials_file)
        self.bucket_name = "imagenes"
    
    def subir_imagen(self, nombre: str, datos: BytesIO, proveedor: str) -> str:
        if proveedor.lower() in ["usa", "us", "estados unidos", "united states"]:
            self.bucket_name = "imagenes-usa"
        else:
            self.bucket_name = "imagenes-lat"
        logger.info(f"Subiendo imagen {nombre} a bucket {self.bucket_name}")
        bucket = self.cliente.bucket(self.bucket_name)
        blob = bucket.blob(nombre)
        blob.upload_from_string(datos.read(), content_type='application/octet-stream')
        url = "gs://%s/%s" % (self.bucket_name, nombre)
        logger.info(f"Succesfully uploaded image to {url}")
        return blob.public_url