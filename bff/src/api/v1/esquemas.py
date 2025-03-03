import typing
import strawberry
import uuid
import requests
import os
from datetime import datetime

from src.utils import obtener_imagenes_anonimizadas

def obtener_todas_imagenes(root) -> typing.List["ImagenAnonimizada"]:
    imagenes_json = obtener_imagenes_anonimizadas()
    imagenes = []

    for imagen in imagenes_json:
        imagenes.append(
            ImagenAnonimizada(
                id=imagen.get('id'),
                nombre_imagen_origen=imagen.get('nombre_imagen_origen'),
                nombre_imagen_destino=imagen.get('nombre_imagen_destino'),
                tamanio_archivo=imagen.get('tamanio_archivo'),
                fecha_creacion=imagen.get('fecha_creacion')
            )
        )
    
    return imagenes

@strawberry.type
class ImagenAnonimizada:
    id: str
    nombre_imagen_origen: str
    nombre_imagen_destino: str
    tamanio_archivo: int
    fecha_creacion: str

@strawberry.type
class IngestaRespuesta:
    mensaje: str
    codigo: int
    id: str = ""

@strawberry.type
class RespuestaAnonimizacion:
    exitoso: bool
    mensaje: str
    codigo: int