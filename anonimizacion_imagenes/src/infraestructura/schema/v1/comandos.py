from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class IngestaImagenPayload(ComandoIntegracion):
    id_usuario = String()
    fecha_creacion= Long()
    id = String()
    filename = String()
    size = String()
    binario = String()
    mimetype = String()

class ComandoIngestaImagen(ComandoIntegracion):
    data = IngestaImagenPayload()

class AnonimizacionRollbackPayload(ComandoIntegracion):
    id = String()

class ComandoAnonimizacionRollback(ComandoIntegracion):
    data = AnonimizacionRollbackPayload()