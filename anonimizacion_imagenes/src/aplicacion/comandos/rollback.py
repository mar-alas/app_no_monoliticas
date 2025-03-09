import logging
from src.infraestructura.gcp_storage import GCPStorage
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen
from src.infraestructura.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import EventoIntegracionImagenAnonimizadaEliminada,ImagenAnonimizadaPayload
from src.infraestructura.schema.v1.comandos import ComandoIngestaRollback
from pulsar.schema import AvroSchema
import time

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
        id_correlacion=mensaje['id_correlacion']

        gCPStorage=GCPStorage()
        nombre_imagen_destino='anonimizada_'+ id_correlacion + '.jpeg'
        
        # se intenta eliminar la imagen anonimizada con una politica de retries
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                gCPStorage.eliminar_imagen(nombre_imagen_destino, proveedor='anonimizador')
                logger.info(f"Imagen {nombre_imagen_destino} eliminada con éxito")
                break
            except Exception as e:
                retries += 1
                if retries < max_retries:
                    logger.warning(f"Error al eliminar imagen, intento {retries}/{max_retries}: {str(e)}") 
                    time.sleep(1 * retries)  # Exponential backoff
                else:
                    logger.error(f"Error al eliminar imagen después de {max_retries} intentos: {str(e)}")
                    raise

        despachador=Despachador()
        payload=ImagenAnonimizadaPayload()
        evento_integracion=EventoIntegracionImagenAnonimizadaEliminada(payload=payload,id_correlacion=id_correlacion)
        avro_schema=AvroSchema(EventoIntegracionImagenAnonimizadaEliminada)
        despachador.publicar_evento(
            evento_integracion=evento_integracion,
            topico='eventos-anonimizador-rollback',
            avro_schema=avro_schema
        )
        
        despachador.publicar_evento(
            evento_integracion=ComandoIngestaRollback(id_correlacion=id_correlacion),
            topico='comando_ingestar_imagenes_rollback',
            avro_schema=AvroSchema(ComandoIngestaRollback)
        )

        
    except Exception as e:
        logger.error(f"Error procesando comando de ingesta: {str(e)}")

