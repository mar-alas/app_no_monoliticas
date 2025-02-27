import datetime
from uuid import uuid4
from src.aplicacion.comandos.crear_imagen_anonimizada import IngestaImagenHandler
from src.aplicacion.dto import IngestaImagenDTO
from src.infraestructura.gcp_storage import GCPStorage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioIngestaImagen:
    def __init__(self):
        self.storage = GCPStorage()
        self.handler = IngestaImagenHandler()
    
    def procesar_y_enviar(self, nombre: str, datos: bytes, proveedor: str, size: int):
        image_id = uuid4()
        logging.info(f"Procesando imagen {image_id}_{nombre} de proveedor {proveedor}")
        url = self.storage.subir_imagen(f"{image_id}_{nombre}", datos, proveedor)
        logger.info(f"Imagen subida a {url}")
        dto = IngestaImagenDTO(
            proveedor=proveedor
        ,   fecha_creacion=datetime.datetime.now()
        ,   id=image_id
        ,   filename=nombre
        ,   size=str(size)
        ,   binario_url=url
        ,   mimetype="image/jpeg"
        )
        self.handler.handle(dto)