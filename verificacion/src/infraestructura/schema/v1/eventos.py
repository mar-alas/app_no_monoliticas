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
    specversion = String(default="v1")
    data = VerificacionResultadoPayload()