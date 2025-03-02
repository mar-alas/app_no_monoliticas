from __future__ import annotations
from dataclasses import dataclass, field
from src.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoDominioImagenAnonimizada:
    def __init__(self, id_imagen, filename, size, fecha_creacion):
        self.id_imagen = id_imagen
        self.filename = filename
        self.size = size
        self.fecha_creacion = fecha_creacion