from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
import uuid
from src.seedwork.infraestructura.utils import time_millis


class AnonimizacionRollbackPayload(ComandoIntegracion):
    id = String()


class ComandoAnonimizacionRollback(ComandoIntegracion):
    id_correlacion= String(default="sin_asignar")
    data = AnonimizacionRollbackPayload()

class AnonimizarImagenPayload(Record):
    id_usuario = String()
    proveedor = String()
    fecha_creacion= Long()
    id = String()
    filename = String()
    size = String()
    binario_url = String()
    mimetype = String()

class ComandoAnonimizarImagen(ComandoIntegracion):
    id_correlacion= String(default="sing_asignar")
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="AnonimizarImagen")
    datacontenttype = String()
    service_name = String(default="anonimizacion_imagenes")
    data = AnonimizarImagenPayload()

class IngestaRollbackPayload(ComandoIntegracion):
    id = String()

class ComandoIngestaRollback(ComandoIntegracion):
    data = IngestaRollbackPayload()