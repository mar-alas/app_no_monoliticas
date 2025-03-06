import uuid
from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.utils import time_millis
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class IngestaImagenPayload(ComandoIntegracion):
    imagen = String()
    fecha_creacion= Long()
    id = String()
    nombre = String()
    proveedor = String()

class ComandoIngestaImagen(ComandoIntegracion):
    id = String()
    time = Long()
    specversion = String()
    type = String()
    ingestion = String()
    datacontenttype = String()
    service_name = String()
    data = IngestaImagenPayload()
