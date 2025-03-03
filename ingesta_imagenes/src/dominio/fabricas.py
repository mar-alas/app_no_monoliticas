
from .entidades import Ingesta
from src.seedwork.dominio.fabricas import Fabrica
from src.seedwork.dominio.repositorios import Mapeador
from src.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaIngestaImagenes(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            ingesta: Ingesta = mapeador.dto_a_entidad(obj)
            return ingesta

@dataclass
class FabricaIngestaImagenes(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Ingesta.__class__:
            fabrica_ingesta_imagenes = _FabricaIngestaImagenes()
            return fabrica_ingesta_imagenes.crear_objeto(obj, mapeador)
        else:
            raise Exception('El objeto no es una Ingesta')