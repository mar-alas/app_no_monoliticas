import logging
from src.infraestructura.gcp_storage import GCPStorage
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rollback(mensaje: dict):
    """
    Procesa los comandos de ingesta de imágenes recibidos del tópico
    
    Args:
        mensaje: Diccionario con la información del comando
    """
    try:
        logger.info(f"Comando de rollback recibido: {mensaje}")
    except Exception as e:
        logger.error(f"Error procesando comando de ingesta: {str(e)}")

