from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

# Payload para el evento de resultado de verificación
class VerificacionResultadoPayload(Record):
    id_verificacion = String()
    id_imagen = String()
    filename = String()
    resultado = String()  # "APROBADA" o "RECHAZADA"
    detalle = String()
    fecha_verificacion = String()

# Evento de integración para la verificación completada
class EventoIntegracionVerificacionCompletada(EventoIntegracion):
    service_name = String(default="verificacion_anonimizacion")
    event_name= String(default="ImagenVerificada")
    specversion = String(default="v1")
    data = VerificacionResultadoPayload()

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