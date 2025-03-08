from src.dominio.fabricas import FabricaIngestaImagenes
from src.dominio.entidades import Ingesta
from src.dominio.repositorios import RepositorioIngesta
from src.infraestructura.dto import IngestaImagenes, Session
from uuid import UUID
from datetime import datetime

class RepositorioIngestaSQLite(RepositorioIngesta):
    def __init__(self):
        self._ingesta_imagen: FabricaIngestaImagenes = FabricaIngestaImagenes()
        self.session = Session()

    @property
    def ingesta_imagen(self):
        return self._ingesta_imagen
    
    def entidad_a_dto(self, entidad: Ingesta) -> IngestaImagenes:
        if isinstance(entidad.fecha_creacion, str):
            fecha_creacion = datetime.fromisoformat(entidad.fecha_creacion)
        else:
            fecha_creacion = entidad.fecha_creacion
        ingesta_dto = IngestaImagenes(
            id=entidad.id,
            filename=entidad.filename,
            size=entidad.size,
            binario_url=entidad.binario_url,
            mimetype=entidad.mimetype,
            fecha_creacion=fecha_creacion,
            proveedor=entidad.proveedor
        )
        return ingesta_dto

    def agregar(self, entity: Ingesta):
        ingesta_dto = self.entidad_a_dto(entity)
        self.session.add(ingesta_dto)
        self.session.commit()

    def actualizar(self, entity: Ingesta):
        ingesta_dto = self.entidad_a_dto(entity)
        self.session.merge(ingesta_dto)
        self.session.commit()

    def eliminar(self, entity: Ingesta):
        ingesta_dto = self.entidad_a_dto(entity)
        self.session.delete(ingesta_dto)
        self.session.commit()

    def obtener_por_id(self, id: UUID) -> Ingesta:
        return self.session.query(IngestaImagenes).filter_by(id=id).first()
    
    def obtener_todos(self):
        return self.session.query(IngestaImagenes).all()