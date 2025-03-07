from dataclasses import dataclass

@dataclass(frozen=True)
class ObjetoValor:
    pass

@dataclass(frozen=True)
class Codigo(ObjetoValor):
    valor: str

@dataclass(frozen=True)
class Ruta(ObjetoValor):
    valor: str

@dataclass(frozen=True)
class Locacion(ObjetoValor):
    valor: str