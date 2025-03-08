from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ImagenIngestadaPayload(Record):
    id_imagen = String()
    filename = String()
    size = String()
    fecha_creacion = String()

class EventoIntegracionImagenIngestada(EventoIntegracion):
    service_name = String(default="ingesta_imagenes")
    event_name= String(default="ImagenIngestada")
    specversion = String(default="v1")
    data = ImagenIngestadaPayload()

class EventoIntegracionImagenIngestadaEliminada(EventoIntegracion):
    service_name = String(default="ingesta_imagenes")
    event_name= String(default="ImagenIngestada")
    specversion = String(default="v1")
    data = ImagenIngestadaPayload()

class FinSagaPayload(Record):
    mensaje = String()

class EventoIntegracionFinSaga(EventoIntegracion):
    service_name = String(default="bff")
    event_name= String(default="FinSaga")
    specversion = String(default="v1")
    data = FinSagaPayload()