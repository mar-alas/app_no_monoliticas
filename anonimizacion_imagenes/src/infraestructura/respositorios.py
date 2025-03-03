from src.infraestructura.dto import DTOImagenAnonimizada, DTOImagenAnonimizadaSchema
from src.config.db import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class RepositorioImagenesAnonimizadasSQLAlchemy():
    def __init__(self):
        DB_USERNAME = os.getenv('DB_USERNAME', default="user")
        DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
        DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
        DB_PORT = os.getenv('DB_PORT', default="9001")
        self.engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/anonimizacion_db')
        
        self.sesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.sesion = self.sesionLocal()

    def almacenar_info_imagen_anonimizada(self, imagen:DTOImagenAnonimizada):
        self.sesion.add(imagen)
        self.sesion.commit()
        self.sesion.refresh(imagen)
        return imagen
    
    def obtener_inventario_imagenes_anonimizadas(self):
        query_schema=DTOImagenAnonimizadaSchema()
        query= self.sesion.query(DTOImagenAnonimizada).all()
        results=query_schema.dump(query,many=True)
        #query_json = [imagen.to_dict() for imagen in query]
        return results
    
    def test_conexion(self):
        try:
            self.engine.connect()
            return True
        except Exception as e:
            return False
    def almacenar_ejemplo(self):
        imagen = DTOImagenAnonimizada(
            fileName="imagen1.jpg",
        )
        self.almacenar_info_imagen_anonimizada(imagen)
        return True
    
