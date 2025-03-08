from src.aplicacion.servicio_ingesta_imagen import ServicioIngestaImagen
from src.infraestructura.consumidores import PulsarSubscriber
from src.seedwork.infraestructura.utils import broker_host
from src.infraestructura.repositorios import RepositorioIngestaSQLite
import os
import logging
import json
import pulsar
import base64
from io import BytesIO
from src.infraestructura.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import ImagenIngestadaPayload,EventoIntegracionImagenIngestada
from pulsar.schema import AvroSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9002")

def process_message(data: bytes):
    try:
        print("Mensaje recibido de cola de comandos de ingestar imagen")
        message = data.decode('utf-8')
        message_dict = json.loads(message)
        payload = message_dict['data']
        nombre = payload['nombre']
        datos_base64 = payload['imagen']
        proveedor = payload['proveedor']
        size = len(datos_base64)

        datos = base64.b64decode(datos_base64)
        datos = BytesIO(base64.b64decode(datos_base64))
        servicio = ServicioIngestaImagen()
        servicio.procesar_y_enviar(nombre=nombre, datos=datos, proveedor=proveedor, size=size)
        despachador=Despachador()

        payload=ImagenIngestadaPayload(
        )
        evento_integracion = EventoIntegracionImagenIngestada(data=payload)
        avro_schema=AvroSchema(EventoIntegracionImagenIngestada)

        despachador.publicar_evento(evento=evento_integracion,topico="eventos-ingesta",avro_schema=avro_schema)
        logger.info("Publicado evento de imagen ingesta")
        logger.info(f"Processed message: {message_dict['id']}")
    except Exception as e:
        logger.error(f"Failed to process message 2: {e}")

if __name__ == '__main__':
    pulsar_host = f'pulsar://{broker_host()}:6650'
    topic = 'public/default/comando_ingestar_imagenes'
    subscription_name = 'my-subscription'

    subscriber = PulsarSubscriber(pulsar_host, topic, subscription_name)
    try:
        subscriber.subscribe(process_message)
    except KeyboardInterrupt:
        subscriber.close()