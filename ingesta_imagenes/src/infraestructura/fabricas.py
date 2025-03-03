from dataclasses import dataclass, field
from src.seedwork.dominio.fabricas import Fabrica
from src.seedwork.dominio.repositorios import Repositorio
from src.dominio.repositorios import RepositorioIngesta
from .repositorios import RepositorioIngestaSQLite

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioIngesta:
            return RepositorioIngestaSQLite()
        else:
            raise Exception("No se puede crear el objeto solicitado")