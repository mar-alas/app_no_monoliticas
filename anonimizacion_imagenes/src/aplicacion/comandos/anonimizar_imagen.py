import logging
from src.infraestructura.gcp_storage import GCPStorage
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def procesar_comando_ingesta(mensaje: dict):
    """
    Procesa los comandos de ingesta de imágenes recibidos del tópico
    
    Args:
        mensaje: Diccionario con la información del comando
    """
    try:
        logger.info(f"Comando de ingesta recibido: {mensaje}")
        gCPStorage=GCPStorage()
        id=mensaje["id"]
        filename=mensaje["filename"]
        proveedor=mensaje["proveedor"]
        nombre=id+"_"+filename
        stream_imagen_sin_anomizar= gCPStorage.descargar_imagen(nombre,proveedor)
        stream_imagen_anonimizada=servicio_anonimizar_imagen(nombre,stream_imagen_sin_anomizar)
        gCPStorage.subir_imagen('anonimizada_'+ nombre,stream_imagen_anonimizada,proveedor)
    except Exception as e:
        logger.error(f"Error procesando comando de ingesta: {str(e)}")

