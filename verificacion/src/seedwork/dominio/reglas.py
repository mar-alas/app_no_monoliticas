from abc import ABC, abstractmethod

class ReglaNegocio(ABC):
    __mensaje: str = "La regla de negocio es invalida"
    
    def __init__(self, mensaje=None):
        if mensaje:
            self.__mensaje = mensaje
            
    def mensaje_error(self) -> str:
        return self.__mensaje
    
    @abstractmethod
    def es_valido(self) -> bool:
        ...
        
    def __bool__(self):
        return self.es_valido()