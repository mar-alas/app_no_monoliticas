import pulsar
from pulsar.schema import *
from . import utils
from src.infraestructura.schema.v1.comandos import ComandoIngestaImagen, IngestaImagenPayload

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoIngestaImagen))
        publicador.send(mensaje)
        cliente.close()

    async def publicar_mensaje(self, comando, topico, schema):
        try:
            payload = IngestaImagenPayload(
                fecha_creacion=comando['data']['fecha_creacion'],
                id=comando['data']['id'],
                nombre=comando['data']['nombre'],
                imagen=comando['data']['imagen'],
                proveedor=comando['data']['proveedor']
            )
            comando_integracion = ComandoIngestaImagen(
                id = comando['id'],
                time = comando['time'],
                specversion = comando['specversion'],
                type = comando['type'],
                datacontenttype = comando['datacontenttype'],
                service_name = comando['service_name'],
                data=payload)
            self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoIngestaImagen))
            return True
        except Exception as e:
            print(f"Error al publicar mensaje: {e}")
            raise