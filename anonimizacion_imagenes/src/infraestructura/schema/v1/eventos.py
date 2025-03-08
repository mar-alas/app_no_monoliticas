from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ImagenAnonimizadaPayload(Record):
    id_imagen = String()
    filename = String()
    size = String()
    fecha_creacion = String()

class EventoIntegracionImagenAnonimizada(EventoIntegracion):
    service_name = String(default="anonimizacion_imagenes")
    event_name= String(default="ImagenAnonimizada")
    specversion = String(default="v1")
    data = ImagenAnonimizadaPayload()

class EventoIntegracionImagenAnonimizadaEliminada(EventoIntegracion):
    service_name = String(default="anonimizacion_imagenes")
    event_name= String(default="ImagenAnonimizadaEliminada")
    specversion = String(default="v1")
    data = ImagenAnonimizadaPayload()