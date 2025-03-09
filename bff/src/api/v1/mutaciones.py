import strawberry
import typing
import uuid
import requests
import base64
from strawberry.types import Info
from src import utils
from src.despachadores import Despachador
from .esquemas import *
from src.infraestructura.schema.v1.comandos import ComandoIngestaImagen, IngestaImagenPayload
from pulsar.schema import AvroSchema
import logging

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def ingestar_imagen(
        self, 
        imagen_base64: str, 
        nombre_imagen: str, 
        proveedor: str = "lat", 
        id_correlacion:str="sin_asignar_2",
        info: Info = None
    ) -> IngestaRespuesta:
        """
        Envía un comando a la cola para ingestar una imagen.
        """
        try:
            # Generar un ID único para esta operación
            id_comando = str(uuid.uuid4())
            
            #TODO eliminar y ordenar
            # Preparar payload del comando
            payload = {
                "imagen": imagen_base64,
                "nombre": nombre_imagen,
                "proveedor": proveedor,
                "id": id_comando,
                "fecha_creacion": utils.time_millis()
            }
            
            # Estructura del comando
            # comando = {
            #     "id": id_comando,
            #     "time": utils.time_millis(),
            #     "specversion": "v1",
            #     "type": "ComandoIngestaImagen",
            #     "datacontenttype": "AVRO",
            #     "service_name": "BFF GraphQL",
            #     "data": payload
            # }
            payload=IngestaImagenPayload(**payload)
            comando=ComandoIngestaImagen(data=payload,id_correlacion=id_correlacion)
            avro_schema=AvroSchema(ComandoIngestaImagen)
            
            # Publicar el comando en la cola
            despachador2 = Despachador()
            await despachador2.publicar_mensaje_avro(
                mensaje=comando,
                topico="comando_ingestar_imagenes",
                avro_schema=avro_schema
            )
            
            return IngestaRespuesta(
                mensaje=f"Comando enviado a la cola con ID: {id_comando}",
                codigo=202  # Accepted - procesando de forma asíncrona
            )
                
        except Exception as e:
            # "error"
            return IngestaRespuesta(
                mensaje=f"Error al enviar comando: {str(e)}",
                codigo=500
            )