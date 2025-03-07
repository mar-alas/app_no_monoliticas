"""Reglas de negocio del dominio de verificación

En este archivo se definen las reglas de negocio para el dominio
de verificación de anonimización
"""

from src.seedwork.dominio.reglas import ReglaNegocio
from datetime import datetime

class IdentificadorDeVerificacionValido(ReglaNegocio):
    identificador: str

    def __init__(self, identificador):
        super().__init__()
        self.identificador = identificador

    def es_valido(self) -> bool:
        if not self.identificador:
            self.mensaje = "El identificador de la verificación no puede estar vacío"
            return False
        return True

class IdentificadorDeImagenValido(ReglaNegocio):
    identificador: str

    def __init__(self, identificador):
        super().__init__()
        self.identificador = identificador

    def es_valido(self) -> bool:
        if not self.identificador:
            self.mensaje = "El identificador de la imagen no puede estar vacío"
            return False
        return True

class NombreDeImagenValido(ReglaNegocio):
    nombre: str

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def es_valido(self) -> bool:
        if not self.nombre:
            self.mensaje = "El nombre de la imagen no puede estar vacío"
            return False
        return True

class FechaVerificacionValida(ReglaNegocio):
    fecha: datetime

    def __init__(self, fecha):
        super().__init__()
        self.fecha = fecha

    def es_valido(self) -> bool:
        if not self.fecha:
            self.mensaje = "La fecha de verificación no puede estar vacía"
            return False
        # La fecha no puede ser en el futuro
        if self.fecha > datetime.now():
            self.mensaje = "La fecha de verificación no puede ser en el futuro"
            return False
        return True