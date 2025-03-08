import datetime
from src.aplicacion.servicio_ingesta_imagen import ServicioIngestaImagen
from src.infraestructura.consumidores import PulsarSubscriber,SuscriptorEventos
from src.seedwork.infraestructura.utils import broker_host, time_millis
from src.infraestructura.repositorios import RepositorioIngestaSQLite
import os
import logging
import json
import pulsar
import base64
from io import BytesIO
from src.infraestructura.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import ImagenIngestadaPayload,EventoIntegracionImagenIngestada,EventoIntegracionImagenIngestadaEliminada,EventoIntegracionFinSaga
from src.infraestructura.schema.v1.comandos import ComandoAnonimizarImagen,AnonimizarImagenPayload,ComandoIngestaImagen,ComandoIngestaRollback
from pulsar.schema import AvroSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9002")

def process_message(data: dict):
    try:
        print("Mensaje recibido de cola de comandos de ingestar imagen")
        message = data
        message_dict = data
        payload = message_dict["data"]
        nombre = payload.nombre
        datos_base64 = payload.imagen
        proveedor = payload.proveedor
        size = len(datos_base64)

        datos = base64.b64decode(datos_base64)
        datos = BytesIO(base64.b64decode(datos_base64))
        servicio = ServicioIngestaImagen()
        image_id,url=servicio.procesar_y_enviar(nombre=nombre, datos=datos, proveedor=proveedor, size=size)
        despachador=Despachador()

        payload=ImagenIngestadaPayload(
        )
        evento_integracion = EventoIntegracionImagenIngestada(data=payload)
        avro_schema=AvroSchema(EventoIntegracionImagenIngestada)

        despachador.publicar_evento(evento=evento_integracion,topico="eventos-ingesta",avro_schema=avro_schema)
        logger.info("Publicado evento de imagen ingesta")
        logger.info(f"Processed message: {message_dict['id']}")

        payload=AnonimizarImagenPayload(
            proveedor=proveedor,
            fecha_creacion= time_millis(),
            id =str(image_id),
            filename = nombre,
            size = str(size),
            binario_url = url,
            mimetype = "image/jpeg"
        )

        evento_integracion = ComandoAnonimizarImagen(data=payload)
        avro_schema=AvroSchema(ComandoAnonimizarImagen)
        despachador.publicar_evento(evento=evento_integracion,topico="comando_anonimizacion_imagenes",avro_schema=avro_schema)

    except Exception as e:
        logger.error(f"Failed to process message 2: {e}")

def rollback(data: dict):
    try:
        print("Mensaje recibido de cola de comandos de rollback")
        despachador=Despachador()
        despachador.publicar_evento(evento=EventoIntegracionImagenIngestadaEliminada(event_name="ImagenIngestadaEliminada"),
                                    topico="eventos-ingesta-rollback",
                                    avro_schema=AvroSchema(EventoIntegracionImagenIngestadaEliminada))
    
        despachador.publicar_evento(evento=EventoIntegracionFinSaga(service_name="ingesta_imagenes"),
                                    topico="eventos-fin-saga",
                                    avro_schema=AvroSchema(EventoIntegracionFinSaga))
    except Exception as e:
        logger.error(f"Failed to rollback: {e}")


def iniciar_suscriptor():
    """Inicializa y configura el suscriptor de eventos"""
    global suscriptor
    try:
        pulsar_host=broker_host()
        suscriptor = SuscriptorEventos(f'pulsar://{pulsar_host}:6650')
        
        suscriptor.suscribirse_a_topico(
            'comando_ingestar_imagenes',
            'ingesta-sub',
            process_message,
            avro_schema=AvroSchema(ComandoIngestaImagen)
        )

        suscriptor.suscribirse_a_topico(
            'comando_ingestar_imagenes_rollback',
            'ingesta-sub',
            rollback,
            avro_schema=AvroSchema(ComandoIngestaRollback)
        )

        logger.info("Suscriptor iniciado correctamente")
    except Exception as e:
        logger.error(f"Error al iniciar suscriptor: {str(e)}")



if __name__ == '__main__':
    try:
        iniciar_suscriptor()

        while True:
            # Sleep to avoid high CPU usage
            import time
            time.sleep(1)

    except KeyboardInterrupt:
        suscriptor.close()