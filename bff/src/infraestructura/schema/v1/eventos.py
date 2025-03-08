from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ImagenAnonimizadaPayload(Record):
    id_imagen = String()
    filename = String()
    size = String()
    fecha_creacion = String()

class EventoIntegracionImagenAnonimizada(EventoIntegracion):
    id_correlacion= String(default="sin_asignar_anonimizacion")
    service_name = String(default="anonimizacion_imagenes")
    event_name= String(default="ImagenAnonimizada")
    specversion = String(default="v1")
    data = ImagenAnonimizadaPayload()

class InicioSagaPayload(Record):
    mensaje = String()

class EventoIntegracionInicioSaga(EventoIntegracion):
    id_correlacion = String(default="sin_asignar_inicio_saga")
    service_name = String(default="bff")
    event_name= String(default="InicioSaga")
    specversion = String(default="v1")
    data = InicioSagaPayload()