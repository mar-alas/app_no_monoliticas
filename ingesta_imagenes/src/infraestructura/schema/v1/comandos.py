import uuid
from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.utils import time_millis
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class IngestaImagenPayload(Record):
    imagen = String()
    nombre = String()
    proveedor = String()
    id = String()
    fecha_creacion= Long()

class ComandoIngestaImagen(ComandoIntegracion):
    id = String()
    time = Long()
    specversion = String()
    type = String()
    ingestion = String()
    datacontenttype = String()
    service_name = String(default="BFF GraphQL")
    data = IngestaImagenPayload()

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
