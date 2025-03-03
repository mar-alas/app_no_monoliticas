from __future__ import annotations
from dataclasses import dataclass, field
from src.seedwork.dominio.entidades import Entidad, AgregacionRaiz
import src.dominio.objetos_valor as ov
from src.dominio.eventos import ImagenIngestada
from datetime import datetime
from uuid import UUID

@dataclass
class Ingesta(AgregacionRaiz):
    id: UUID = field(default_factory=UUID)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    filename: str = field(default=None)
    size: str = field(default=None)
    binario_url: str = field(default=None)
    mimetype: str = field(default=None)
    proveedor: str = field(default=None)

    def ingestar_imagen(self):
        self.agregar_evento(ImagenIngestada(proveedor=self.proveedor, fecha_creacion=self.fecha_creacion, id=self.id,
                                            filename=self.filename, size=self.size, binario_url=self.binario_url,
                                            mimetype=self.mimetype))