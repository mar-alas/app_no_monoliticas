"""Reglas de negocio reusables parte del seedwork del proyecto

En este archivo usted encontrará reglas de negocio reusables parte del seedwork del proyecto

"""

from abc import ABC, abstractmethod

class ReglaNegocio(ABC):

    __mensaje: str ='La regla de negocio es invalida'

    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def mensaje_error(self) -> str:
        return self.__mensaje

    @abstractmethod
    def es_valido(self) -> bool:
        ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__mensaje}"


        
class NombreDeImagenNoPuedeSerVacio(ReglaNegocio):

    nombre: str

    def __init__(self, nombre, mensaje='El nombre de la imagen no puede ser vacio'):
        super().__init__(mensaje)
        self.nombre = nombre

    def es_valido(self) -> bool:
        if self.nombre == '':
            return False
        return True
    
class TamanioDeImagenEsValido(ReglaNegocio):

    tamanio: int

    def __init__(self, tamanio, mensaje='El tamaño de la imagen no es valido'):
        super().__init__(mensaje)
        self.tamanio = tamanio

    def es_valido(self) -> bool:
        if self.tamanio <= 0:
            return False
        return True
    
class FormatoDeImagenEsValido(ReglaNegocio):
    formato: str

    def __init__(self, formato, mensaje='El formato de la imagen no es valido'):
        super().__init__(mensaje)
        self.formato = formato
    
    def es_valido(self) -> bool:
        if not self.formato or '.' not in self.formato:
            return False
            
        extension = self.formato.split('.')[-1].lower()
        return extension in ['jpg', 'jpeg', 'png']

class ImagenDeAnonimizacionEsValida(ReglaNegocio):

    imagen: bytes

    def __init__(self, imagen, mensaje='La imagen de anonimizacion no es valida'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido(self) -> bool:
        if self.imagen is None:
            return False
        return True
