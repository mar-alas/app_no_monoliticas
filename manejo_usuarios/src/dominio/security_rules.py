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
    RANGO_IPS_PERMITIDAS: List[str] = [
        "123.456.789.000", "123.456.789.001", "123.456.789.002", "123.456.789.003", "123.456.789.004",
        "123.456.789.005", "123.456.789.006", "123.456.789.007", "123.456.789.008", "123.456.789.009",
        "123.456.789.010", "123.456.789.011", "123.456.789.012", "123.456.789.013", "123.456.789.014",
        "123.456.789.015", "123.456.789.016", "123.456.789.017", "123.456.789.018", "123.456.789.019",
        "123.456.789.020", "123.456.789.021", "123.456.789.022", "123.456.789.023", "123.456.789.024",
        "123.456.789.025", "123.456.789.026", "123.456.789.027", "123.456.789.028", "123.456.789.029",
        "123.456.789.030", "123.456.789.031", "123.456.789.032", "123.456.789.033", "123.456.789.034",
        "123.456.789.035", "123.456.789.036", "123.456.789.037", "123.456.789.038", "123.456.789.039",
        "123.456.789.040", "123.456.789.041", "123.456.789.042", "123.456.789.043", "123.456.789.044",
        "123.456.789.045", "123.456.789.046", "123.456.789.047", "123.456.789.048", "123.456.789.049",
        "123.456.789.050", "123.456.789.051", "123.456.789.052", "123.456.789.053", "123.456.789.054",
        "123.456.789.055", "123.456.789.056", "123.456.789.057", "123.456.789.058", "123.456.789.059",
        "123.456.789.060", "123.456.789.061", "123.456.789.062", "123.456.789.063", "123.456.789.064",
        "123.456.789.065", "123.456.789.066", "123.456.789.067", "123.456.789.068", "123.456.789.069",
        "123.456.789.070", "123.456.789.071", "123.456.789.072", "123.456.789.073", "123.456.789.074",
        "123.456.789.075", "123.456.789.076", "123.456.789.077", "123.456.789.078", "123.456.789.079",
        "123.456.789.080", "123.456.789.081", "123.456.789.082", "123.456.789.083", "123.456.789.084",
        "123.456.789.085", "123.456.789.086", "123.456.789.087", "123.456.789.088", "123.456.789.089",
        "123.456.789.090", "123.456.789.091", "123.456.789.092", "123.456.789.093", "123.456.789.094",
        "123.456.789.095", "123.456.789.096", "123.456.789.097", "123.456.789.098", "123.456.789.099"
    ]


    def __init__(self, ip: str, mensaje='La dirección IP no está permitida'):
        super().__init__(mensaje)
        self.ip = ip

    def es_valido(self) -> bool:
        return self.ip in self.RANGO_IPS_PERMITIDAS