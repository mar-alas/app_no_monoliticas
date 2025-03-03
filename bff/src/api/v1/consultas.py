import strawberry
import typing
from src.api.v1.esquemas import *

@strawberry.type
class Query:
    imagenes_anonimizadas: typing.List[ImagenAnonimizada] = strawberry.field(resolver=obtener_todas_imagenes)