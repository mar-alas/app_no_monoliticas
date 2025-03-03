from src.seedwork.aplicacion.dto import Mapeador as AppMap
from src.seedwork.dominio.repositorios import Mapeador as RepMap
from src.dominio.entidades import Ingesta
from src.dominio.objetos_valor import Ingesta, Odo, Segmento, Leg
from .dto import IngestaImagenDTO

from datetime import datetime


class MapeadorIngesta(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%S.%f'

    def _procesar_ingesta(self, ingesta_dto: IngestaImagenDTO) -> Ingesta:
        fecha_creacion = datetime.strptime(ingesta_dto.fecha_creacion, self._FORMATO_FECHA)
        return Ingesta(
                    id=ingesta_dto.id,
                    filename=ingesta_dto.filename,
                    size=ingesta_dto.size,
                    binario_url=ingesta_dto.binario_url,
                    mimetype=ingesta_dto.mimetype,
                    fecha_creacion=fecha_creacion,
                    proveedor=ingesta_dto.proveedor
        )

    def dto_a_entidad(self, dto: IngestaImagenDTO) -> Ingesta:
        return self._procesar_ingesta(dto)

    def entidad_a_dto(self, entidad: Ingesta) -> IngestaImagenDTO:
        return IngestaImagenDTO(
            id=entidad.id,
            filename=entidad.filename,
            size=entidad.size,
            binario_url=entidad.binario_url,
            mimetype=entidad.mimetype,
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            proveedor=entidad.proveedor
        )

    def obtener_tipo(self) -> type:
        return Ingesta