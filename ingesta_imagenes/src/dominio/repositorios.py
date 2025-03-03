""" Interfaces para los repositorios del dominio de ingesta de imágenes

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de ingesta de imagenes

"""

from abc import ABC
from src.seedwork.dominio.repositorios import Repositorio

class RepositorioIngesta(Repositorio, ABC):
    ...