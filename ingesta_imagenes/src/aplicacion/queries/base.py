from src.seedwork.aplicacion.queries import QueryHandler
from src.infraestructura.fabricas import FabricaRepositorio
from src.dominio.fabricas import FabricaIngestaImagenes

class IngestaBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repsitorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingesta: FabricaIngestaImagenes = FabricaIngestaImagenes()

    @property
    def fabrica_ingesta(self):
        return self._fabrica_ingesta
    
    @property
    def fabrica_repositorio(self):
        return self._fabrica_repsitorio    