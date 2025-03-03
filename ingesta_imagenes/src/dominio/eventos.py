from __future__ import annotations
from dataclasses import dataclass, field
from src.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid

@dataclass
class ImagenIngestada(EventoDominio):
    id: uuid.UUID = None
    proveedor: str = None
    fecha_creacion: datetime = None
    filename: str = None
    size: str = None
    binario_url: str = None
    mimetype: str = None