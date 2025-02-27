import pulsar
from pulsar.schema import *
from avro.io import DatumWriter, BinaryEncoder
from io import BytesIO
from ingesta_imagenes.src.infraestructura.schema.v1.comandos import IngestaImagenPayload, ComandoIngestaImagen
from src.seedwork.infraestructura import utils
import logging

import datetime
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoIngestaImagen))
        publicador.send(mensaje)
        cliente.close()
    
    def publicar_comando(self, comando, topico):
        payload = IngestaImagenPayload(
            fecha_creacion=unix_time_millis(datetime.datetime.now()),
            id_usuario=comando.id_usuario,
            id=comando.id,
            filename=comando.filename,
            size=comando.size,
            binario=comando.binario,
            mimetype=comando.mimetype
        )
        from pdb import set_trace; set_trace()
        comando_integracion = ComandoIngestaImagen(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoIngestaImagen))
