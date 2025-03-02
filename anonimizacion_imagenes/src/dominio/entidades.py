from src.seedwork.dominio.entidades import Entidad
import src.dominio.objetos_valor as ov
from dataclasses import dataclass, field

@dataclass
class EntidadImagenAnonimizada(Entidad):
    filename: ov.fileName = field(default_factory=ov.fileName)