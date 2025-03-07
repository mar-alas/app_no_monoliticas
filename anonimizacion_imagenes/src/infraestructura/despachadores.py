import pulsar
from pulsar.schema import *

from src.infraestructura.schema.v1.eventos import EventoIntegracionImagenAnonimizada, ImagenAnonimizadaPayload
from src.seedwork.infraestructura import utils
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento_integracion:EventoIntegracion, topico,avro_schema):
        self._publicar_mensaje(evento_integracion, topico, avro_schema)