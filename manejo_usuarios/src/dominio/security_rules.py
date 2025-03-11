from abc import ABC, abstractmethod
from typing import List

class ReglaNegocio(ABC):
    __mensaje: str = 'La regla de negocio es inválida'

    def __init__(self, mensaje: str):
        self.__mensaje = mensaje

    def mensaje_error(self) -> str:
        return self.__mensaje

    @abstractmethod
    def es_valido(self) -> bool:
        ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__mensaje}"


class PaisNoPermitido(ReglaNegocio):
    PAISES_PERMITIDOS: List[str] = [
        'US', 'MX', 'GT', 'SV', 'HN', 'NI', 'CR', 'PA', 'CO', 'VE', 'EC', 'PE', 'BO', 'PY', 'UY', 'AR', 'CL', 'BR', 'DO'
    ]

    def __init__(self, pais: str, mensaje='El país de origen no está permitido'):
        super().__init__(mensaje)
        self.pais = pais

    def es_valido(self) -> bool:
        return self.pais in self.PAISES_PERMITIDOS


class NavegadorNoPermitido(ReglaNegocio):
    NAVEGADORES_PERMITIDOS: List[str] = ['chrome', 'safari']

    def __init__(self, navegador: str, mensaje='El navegador no está permitido'):
        super().__init__(mensaje)
        self.navegador = navegador.lower()

    def es_valido(self) -> bool:
        return self.navegador in self.NAVEGADORES_PERMITIDOS


class SistemaOperativoNoPermitido(ReglaNegocio):
    SISTEMAS_PERMITIDOS: List[str] = ['windows', 'macos']

    def __init__(self, sistema: str, mensaje='El sistema operativo no está permitido'):
        super().__init__(mensaje)
        self.sistema = sistema.lower()

    def es_valido(self) -> bool:
        return self.sistema in self.SISTEMAS_PERMITIDOS


class DominioCorreoNoPermitido(ReglaNegocio):
    DOMINIOS_PERMITIDOS: List[str] = ['uniandes.edu.co', 'saludtech.com']

    def __init__(self, correo: str, mensaje='El dominio de correo no está permitido'):
        super().__init__(mensaje)
        self.correo = correo

    def es_valido(self) -> bool:
        dominio = self.correo.split('@')[-1]
        return dominio in self.DOMINIOS_PERMITIDOS


class IPNoPermitida(ReglaNegocio):
    RANGO_IPS_PERMITIDAS: List[str] = [f"123.456.789.{i:03d}" for i in range(101)]

    def __init__(self, ip: str, mensaje='La dirección IP no está permitida'):
        super().__init__(mensaje)
        self.ip = ip

    def es_valido(self) -> bool:
        return self.ip in self.RANGO_IPS_PERMITIDAS