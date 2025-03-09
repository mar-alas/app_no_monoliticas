from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

# Payload para solicitar manualmente una verificación
class SolicitarVerificacionPayload(Record):
    id_imagen = String()
    filename = String()
    proveedor = String()

# Comando de integración para solicitar una verificación
class ComandoSolicitarVerificacion(ComandoIntegracion):
    data = SolicitarVerificacionPayload()

class AnonimizacionRollbackPayload(ComandoIntegracion):
    id = String()


class ComandoAnonimizacionRollback(ComandoIntegracion):
    id_correlacion= String(default="sin_asignar")
    data = AnonimizacionRollbackPayload()