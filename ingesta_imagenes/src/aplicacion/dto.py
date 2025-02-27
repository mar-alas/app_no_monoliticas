from dataclasses import dataclass, field
from src.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class IngestaImagenDTO(DTO):
    proveedor: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    filename: str = field(default_factory=str)
    size: str = field(default_factory=str)
    binario_url: str = field(default_factory=str)
    mimetype: str = field(default_factory=str)


