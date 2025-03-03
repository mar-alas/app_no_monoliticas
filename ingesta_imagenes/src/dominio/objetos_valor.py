from __future__ import annotations

from dataclasses import dataclass, field
from src.seedwork.dominio.objetos_valor import ObjetoValor, Imagen
from datetime import datetime
from enum import Enum


@dataclass(frozen=True)
class fileName():
    nombre: str

@dataclass(frozen=True)
class Ingesta(ObjetoValor):
    odos: list[Odo] = field(default_factory=list)

@dataclass(frozen=True)
class Leg(Imagen):
    filename: fileName

@dataclass(frozen=True)
class Segmento(Imagen):
    legs: list[Leg]

@dataclass(frozen=True)
class Odo(Imagen):
    segmentos: list[Segmento]
