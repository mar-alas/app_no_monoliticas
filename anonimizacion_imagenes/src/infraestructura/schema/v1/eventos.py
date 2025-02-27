from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ImagenAnonimizadaPayload(Record):
    id_imagen = String()
    filename = String()
    size = String()
    fecha_creacion = Long()

class ImagenAnonimizada(EventoIntegracion):
    data = ImagenAnonimizadaPayload()