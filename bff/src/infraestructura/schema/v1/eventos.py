from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ImagenAnonimizadaPayload(Record):
    id_imagen = String()
    filename = String()
    size = String()
    fecha_creacion = String()

class EventoIntegracionImagenAnonimizada(EventoIntegracion):
    service_name = String(default="anonimizacion_imagenes")
    specversion = String(default="v1")
    data = ImagenAnonimizadaPayload()