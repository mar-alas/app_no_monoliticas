import pulsar
from pulsar.schema import *
from . import utils

class Despachador:
    async def publicar_mensaje(self, mensaje, topico, schema):
        try:
            # Obtener el schema del registro
            try:
                json_schema = utils.consultar_schema_registry(schema)  
                avro_schema = utils.obtener_schema_avro_de_diccionario(json_schema)
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
            raise