"""Objetos valor del dominio de verificación

En este archivo se encuentran los objetos valor del dominio de verificación de anonimización
"""

from __future__ import annotations

from dataclasses import dataclass, field
from src.seedwork.dominio.objetos_valor import ObjetoValor
from enum import Enum

class EstadoVerificacion(Enum):
    """Estados posibles de una verificación"""
    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"
    ERROR = "ERROR"

@dataclass(frozen=True)
class NombreImagen(ObjetoValor):
    """Objeto valor que representa el nombre de una imagen"""
    valor: str = ""

@dataclass(frozen=True)
class ResultadoVerificacion(ObjetoValor):
    """
    Objeto valor que representa el resultado de una verificación
    
    Attributes:
        estado: Estado de la verificación (PENDIENTE, APROBADA, RECHAZADA, ERROR)
        detalle: Detalles adicionales sobre el resultado
    """
    estado: EstadoVerificacion = EstadoVerificacion.PENDIENTE
    detalle: str = ""
    
    @staticmethod
    def aprobada(detalle: str = "") -> ResultadoVerificacion:
        """Crea un resultado de verificación aprobada"""
        return ResultadoVerificacion(estado=EstadoVerificacion.APROBADA, detalle=detalle)
    
    @staticmethod
    def rechazada(detalle: str = "") -> ResultadoVerificacion:
        """Crea un resultado de verificación rechazada"""
        return ResultadoVerificacion(estado=EstadoVerificacion.RECHAZADA, detalle=detalle)
    
    @staticmethod
    def error(detalle: str = "") -> ResultadoVerificacion:
        """Crea un resultado de verificación con error"""
        return ResultadoVerificacion(estado=EstadoVerificacion.ERROR, detalle=detalle)