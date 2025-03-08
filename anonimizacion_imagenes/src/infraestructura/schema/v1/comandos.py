from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
import uuid
from src.seedwork.infraestructura.utils import time_millis

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

class AnonimizarImagenPayload(Record):
    id_usuario = String()
    fecha_creacion= Long()
    id = String()
    filename = String()
    size = String()
    binario_url = String()
    mimetype = String()

class ComandoAnonimizarImagen(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="AnonimizarImagen")
    datacontenttype = String()
    service_name = String(default="anonimizacion_imagenes")
    data = AnonimizarImagenPayload()