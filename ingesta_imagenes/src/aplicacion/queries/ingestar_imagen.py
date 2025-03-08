from src.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from src.seedwork.aplicacion.queries import ejecutar_query as query
from src.infraestructura.repositorios import RepositorioIngestaSQLite
from src.infraestructura.fabricas import FabricaRepositorio
from src.dominio.entidades import Ingesta
from dataclasses import dataclass
from .base import IngestaBaseHandler
import uuid

@dataclass
class ObtenerIngesta(Query):
    id: str

class ObtenerIngestaHandler(IngestaBaseHandler):

    def handle(self, query: ObtenerIngesta) -> QueryResultado:
        # Implement the logic to handle the query
        repositorio = FabricaRepositorio.crear_repositorio_ingesta()
        ingesta = repositorio.obtener_por_id(query.id)
        return QueryResultado(resultado=ingesta)

@query.register(ObtenerIngesta)
def ejecutar_query_obtener_ingesta(query: ObtenerIngesta):
    handler = ObtenerIngestaHandler()
    return handler.handle(query)