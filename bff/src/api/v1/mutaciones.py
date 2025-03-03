import strawberry
import typing
import uuid
from strawberry.types import Info
from src.despachadores import Despachador
from .esquemas import *

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def ingestar_imagen(self, info: Info) -> IngestaRespuesta:
        # Este método se implementará la ingesta de imágenes
        
        return IngestaRespuesta(
            mensaje="Funcionalidad en desarrollo", 
            codigo=501
        )