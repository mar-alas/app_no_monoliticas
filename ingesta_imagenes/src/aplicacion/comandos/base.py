from src.seedwork.aplicacion.comandos import ComandoHandler
from src.infraestructura.fabricas import FabricaRepositorio

class IngestaImagenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio