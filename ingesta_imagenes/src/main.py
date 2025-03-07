from src.aplicacion.servicio_ingesta_imagen import ServicioIngestaImagen
from src.infraestructura.consumidores import PulsarSubscriber
from src.seedwork.infraestructura.utils import broker_host
import os
import logging
import json
import pulsar
import base64
from io import BytesIO

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
        logger.info(f"Processed message: {message_dict}")
    except Exception as e:
        logger.error(f"Failed to process message: {e}")

if __name__ == '__main__':
    pulsar_host = f'pulsar://{broker_host()}:6650'
    topic = 'public/default/comando_ingestar_imagenes'
    subscription_name = 'my-subscription'

    subscriber = PulsarSubscriber(pulsar_host, topic, subscription_name)
    try:
        subscriber.subscribe(process_message)
    except KeyboardInterrupt:
        subscriber.close()

