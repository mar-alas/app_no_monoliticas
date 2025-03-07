import pulsar
from pulsar.schema import *
from . import utils
from src.infraestructura.schema.v1.comandos import ComandoIngestaImagen, IngestaImagenPayload
import json

class Despachador:
    async def publicar_mensaje(self, mensaje, topico, schema):
        try:
            # Obtener el schema del registro
            try:
                json_schema = utils.consultar_schema_registry(schema)
                avro_schema = utils.obtener_schema_avro_de_diccionario(json_schema)
                avro_schema = None
            except Exception as e:
                print(f"Error obteniendo schema, usando AvroSchema genérico: {e}")
                # Si no se puede obtener el schema, usamos un AvroSchema genérico
                avro_schema = None
                 # Conectar pulsar y publicar
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

            # Si tenemos un schema, lo usamos, sino publicamos sin schema
            if avro_schema:
                publicador = cliente.create_producer(topico, schema=avro_schema)
            else:
                publicador = cliente.create_producer(topico)
                # Convertir el mensaje a JSON
                if not isinstance(mensaje, str):
                    import json
                    mensaje = json.dumps(mensaje)
                    mensaje = mensaje.encode('utf-8')

            publicador.send(mensaje)
            cliente.close()
            return True
        except Exception as e:
            print(f"Error al publicar mensaje: {e}")

    # def _publicar_mensaje(self, mensaje, topico, schema):
    #     cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
    #     publicador = cliente.create_producer(topico) # schema=AvroSchema(ComandoIngestaImagen))
    #     mensaje = json.dumps(mensaje)
    #     mensaje = mensaje.encode('utf-8')
    #     publicador.send(mensaje)
    #     cliente.close()

    # async def publicar_mensaje(self, comando, topico, schema):
    #     try:
    #         payload = IngestaImagenPayload(
    #             fecha_creacion=comando['data']['fecha_creacion'],
    #             id=comando['data']['id'],
    #             nombre=comando['data']['nombre'],
    #             imagen=comando['data']['imagen'],
    #             proveedor=comando['data']['proveedor']
    #         )
    #         comando_integracion = ComandoIngestaImagen(
    #             id = comando['id'],
    #             time = comando['time'],
    #             specversion = comando['specversion'],
    #             type = comando['type'],
    #             datacontenttype = comando['datacontenttype'],
    #             service_name = comando['service_name'],
    #             data=payload)
    #         self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoIngestaImagen))
    #         return True
    #     except Exception as e:
    #         print(f"Error al publicar mensaje: {e}")
    #         raise