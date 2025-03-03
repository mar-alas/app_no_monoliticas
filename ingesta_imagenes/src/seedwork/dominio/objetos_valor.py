from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class ObjetoValor:
    ...

@dataclass(frozen=True)
class Imagen(ABC, ObjetoValor):
    ...