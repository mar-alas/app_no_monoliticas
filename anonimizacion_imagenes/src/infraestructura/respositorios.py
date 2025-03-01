from src.infraestructura.dto import ImagenAnonimizada as ImagenAnonimizadaDTO
from src.config.db import db

class RepositorioImagenesAnonimizadasSQLAlchemy():
    def almacenar_info_imagen_anonimizada(self, imagen:ImagenAnonimizadaDTO):
        db.session.add(imagen)
        db.session.commit()