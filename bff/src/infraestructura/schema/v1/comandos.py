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
