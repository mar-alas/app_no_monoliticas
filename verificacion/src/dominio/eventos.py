from __future__ import annotations
from dataclasses import dataclass, field
from src.seedwork.dominio.eventos import EventoDominio
from datetime import datetime

class EventoDominioVerificacion(EventoDominio):
    """Clase base para los eventos de dominio de verificación"""
    ...

@dataclass
class VerificacionCreada(EventoDominioVerificacion):
    """Evento que se emite cuando se crea una verificación"""
    id_verificacion: str = ""
    id_imagen: str = ""
    nombre_imagen: str = ""
    fecha_creacion: datetime = field(default_factory=datetime.now)

@dataclass
class VerificacionCompletada(EventoDominioVerificacion):
    """Evento que se emite cuando se completa una verificación"""
    id_verificacion: str = ""
    id_imagen: str = ""
    nombre_imagen: str = ""
    resultado: str = ""  # APROBADA, RECHAZADA
    detalle: str = ""
    fecha_verificacion: datetime = field(default_factory=datetime.now)