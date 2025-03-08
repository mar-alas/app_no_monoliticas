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
    
    def obtener_imagen_anonimizada(self, nombre: str, proveedor: str) -> BytesIO:
        """
        Obtiene una imagen anonimizada del bucket correspondiente
        
        Args:
            nombre: Nombre de la imagen anonimizada
            proveedor: Proveedor (determina el bucket)
            
        Returns:
            BytesIO: Stream con los datos de la imagen
        """
        # El nombre ya debe incluir el prefijo 'anonimizada_'
        if not nombre.startswith('anonimizada_'):
            nombre = 'anonimizada_' + nombre
            
        if proveedor.lower() in ["usa", "us", "estados unidos", "united states"]:
            self.bucket_name = "imagenes-usa"
        else:
            self.bucket_name = "imagenes-lat"
            
        logger.info(f"Descargando imagen anonimizada {nombre} de bucket {self.bucket_name}")
        
        bucket = self.cliente.bucket(self.bucket_name)
        blob = bucket.blob(nombre)
        datos = BytesIO()
        blob.download_to_file(datos)
        datos.seek(0)
        
        logger.info(f"Imagen anonimizada {nombre} descargada exitosamente")
        
        return datos