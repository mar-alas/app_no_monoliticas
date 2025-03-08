from src.seedwork.dominio.entidades import Entidad
import src.dominio.objetos_valor as ov
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EntidadVerificacion(Entidad):
    """
    Entidad que representa una verificación de anonimización de imagen
    """
    id_imagen: str = field(default="")
    nombre_imagen: ov.NombreImagen = field(default_factory=ov.NombreImagen)
    resultado: ov.ResultadoVerificacion = field(default_factory=ov.ResultadoVerificacion)
    fecha_verificacion: datetime = field(default_factory=datetime.now)
    proveedor: str = field(default="")