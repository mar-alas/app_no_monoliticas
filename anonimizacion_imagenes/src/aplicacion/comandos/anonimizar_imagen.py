import logging
from src.infraestructura.gcp_storage import GCPStorage
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def procesar_comando_anonimizacion(mensaje: dict):
    """
    Procesa los comandos de anonimizacion recibidos del tópico
    
    Args:
        mensaje: Diccionario con la información del comando
    """
    try:
        logger.info(f"Comando de ingesta recibido: {mensaje}")
        payload=mensaje["data"]
        id_correlacion=mensaje["id_correlacion"]
        gCPStorage=GCPStorage()
        id=payload.id
        filename=payload.filename
        proveedor=payload.proveedor
        nombre_imagen_origen=id+"_"+filename
        nombre_imagen_destino='anonimizada_'+ nombre_imagen_origen
        stream_imagen_sin_anomizar= gCPStorage.descargar_imagen(nombre_imagen_origen,proveedor)
        stream_imagen_anonimizada=servicio_anonimizar_imagen(nombre_imagen_origen,nombre_imagen_destino,stream_imagen_sin_anomizar,id_correlacion=id_correlacion)
        gCPStorage.subir_imagen('anonimizada_'+ nombre_imagen_origen,stream_imagen_anonimizada,proveedor)
    except Exception as e:
        logger.error(f"Error procesando comando de ingesta AAA: {str(e)}")

