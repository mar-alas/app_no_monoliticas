from pulsar.schema import *
import time
import uuid

def time_millis():
    return int(time.time() * 1000)

class Mensaje(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

class EventoIntegracion(Mensaje):
    ...

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

class ImagenIngestadaPayload(Record):
    id_imagen = String()
    filename = String()
    size = String()
    fecha_creacion = String()

class EventoIntegracionImagenIngestada(EventoIntegracion):
    id_correlacion= String(default="sin_asignar_ingesta")
    service_name = String(default="ingesta_imagenes")
    event_name= String(default="ImagenIngestada")
    specversion = String(default="v1")
    data = ImagenIngestadaPayload()

class InicioSagaPayload(Record):
    mensaje = String()

class EventoIntegracionInicioSaga(EventoIntegracion):
    id_correlacion = String(default="sin_asignar_inicio_saga")
    service_name = String(default="bff")
    event_name= String(default="InicioSaga")
    specversion = String(default="v1")
    data = InicioSagaPayload()

class EventoIntegracionImagenAnonimizadaEliminada(EventoIntegracion):
    id_correlacion= String(default="sin_asignar_anonimizacion")
    service_name = String(default="anonimizacion_imagenes")
    event_name= String(default="ImagenAnonimizadaEliminada")
    specversion = String(default="v1")
    data = ImagenAnonimizadaPayload()


class VerificacionResultadoPayload(Record):
    id_verificacion = String()
    id_imagen = String()
    filename = String()
    resultado = String()  # "APROBADA" o "RECHAZADA"
    detalle = String()
    fecha_verificacion = String()


class EventoIntegracionVerificacionCompletada(EventoIntegracion):
    id_correlacion= String(default="sin_asignar_anonimizacion")
    service_name = String(default="verificacion_anonimizacion")
    event_name= String(default="ImagenVerificada")
    specversion = String(default="v1")
    data = VerificacionResultadoPayload()

class FinSagaPayload(Record):
    mensaje = String()

class EventoIntegracionFinSaga(EventoIntegracion):
    id_correlacion= String(default="sin_asignar_anonimizacion")
    service_name = String(default="bff")
    event_name= String(default="FinSaga")
    specversion = String(default="v1")
    data = FinSagaPayload()


class EventoIntegracionImagenIngestadaEliminada(EventoIntegracion):
    id_correlacion= String(default="sin_asignar_ingesta")
    service_name = String(default="ingesta_imagenes")
    event_name= String(default="ImagenIngestada")
    specversion = String(default="v1")
    data = ImagenIngestadaPayload()