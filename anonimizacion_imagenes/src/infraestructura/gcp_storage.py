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
credentials_file = ".keys/key.json"

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

    def descargar_imagen(self, nombre: str, proveedor: str)-> BytesIO:
        '''
        nombre: nombre de la imagen a descargar, ej:4d17a605-e9d3-46be-883d-7418fce7ea50_test_image.jpeg
        '''
        if proveedor.lower() in ["usa", "us", "estados unidos", "united states"]:
            self.bucket_name = "imagenes-usa"
        else:
            self.bucket_name = "imagenes-lat"
        logger.info(f"Descargando imagen {nombre} de bucket {self.bucket_name}")
        bucket = self.cliente.bucket(self.bucket_name)
        blob = bucket.blob(nombre)
        datos = BytesIO()
        blob.download_to_file(datos)
        datos.seek(0)
        logger.info(f"Succesfully downloaded image {nombre} from {self.bucket_name}")

        return datos
    
    def eliminar_imagen(self, nombre: str, proveedor: str):
        if proveedor.lower() in ["usa", "us", "estados unidos", "united states"]:
            self.bucket_name = "imagenes-usa"
        else:
            self.bucket_name = "imagenes-lat"
        logger.info(f"Eliminando imagen {nombre} de bucket {self.bucket_name}")
        bucket = self.cliente.bucket(self.bucket_name)
        blob = bucket.blob(nombre)
        blob.delete()
        logger.info(f"Succesfully deleted image {nombre} from {self.bucket_name}")
        

        