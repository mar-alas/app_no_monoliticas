import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from src.infraestructura.dto import DTOVerificacion, DTOVerificacionSchema, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepositorioVerificacionesSQLAlchemy:
    """Repositorio para el almacenamiento y consulta de verificaciones"""
    
    def __init__(self):
        # Configuración de conexión
        DB_USERNAME = os.getenv('DB_USERNAME', default="user")
        DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
        DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
        DB_PORT = os.getenv('DB_PORT', default="9003")
        
        # Conexión a la base de datos
        self.engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/verificacion_db')
        
        # Crear las tablas si no existen
        Base.metadata.create_all(self.engine)
        
        # Configurar la sesión
        self.sesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.sesion = self.sesionLocal()
    
    def crear(self, verificacion: DTOVerificacion) -> DTOVerificacion:
        """
        Crea una nueva verificación en la base de datos
        
        Args:
            verificacion: DTO con la información de la verificación
            
        Returns:
            DTOVerificacion: La verificación creada
        """
        try:
            self.sesion.add(verificacion)
            self.sesion.commit()
            self.sesion.refresh(verificacion)
            logger.info(f"Verificación creada: {verificacion.id}")
            return verificacion
        except Exception as e:
            self.sesion.rollback()
            logger.error(f"Error al crear verificación: {str(e)}")
            raise
    
    def obtener_por_id(self, id_verificacion: str) -> DTOVerificacion:
        """
        Obtiene una verificación por su ID
        
        Args:
            id_verificacion: ID de la verificación
            
        Returns:
            DTOVerificacion: La verificación encontrada o None
        """
        return self.sesion.query(DTOVerificacion).filter(DTOVerificacion.id == id_verificacion).first()
    
    def obtener_por_imagen(self, id_imagen: str) -> list:
        """
        Obtiene las verificaciones relacionadas con una imagen
        
        Args:
            id_imagen: ID de la imagen
            
        Returns:
            list: Lista de verificaciones relacionadas con la imagen
        """
        return self.sesion.query(DTOVerificacion).filter(DTOVerificacion.id_imagen == id_imagen).all()
    
    def obtener_todas(self) -> list:
        """
        Obtiene todas las verificaciones
        
        Returns:
            list: Lista con todas las verificaciones
        """
        verificaciones = self.sesion.query(DTOVerificacion).all()
        return verificaciones
    
    def obtener_todas_serializadas(self) -> list:
        """
        Obtiene todas las verificaciones en formato serializable (dict)
        
        Returns:
            list: Lista con todas las verificaciones serializadas
        """
        verificaciones = self.obtener_todas()
        schema = DTOVerificacionSchema()
        return schema.dump(verificaciones, many=True)
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas sobre las verificaciones
        
        Returns:
            dict: Estadísticas de verificaciones
        """
        total = self.sesion.query(DTOVerificacion).count()
        aprobadas = self.sesion.query(DTOVerificacion).filter(DTOVerificacion.resultado == "APROBADA").count()
        rechazadas = self.sesion.query(DTOVerificacion).filter(DTOVerificacion.resultado == "RECHAZADA").count()
        
        return {
            "total": total,
            "aprobadas": aprobadas,
            "rechazadas": rechazadas,
            "porcentaje_aprobadas": (aprobadas / total) * 100 if total > 0 else 0,
            "porcentaje_rechazadas": (rechazadas / total) * 100 if total > 0 else 0
        }
    
    def test_conexion(self) -> bool:
        """
        Prueba la conexión a la base de datos
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            self.engine.connect()
            return True
        except Exception as e:
            logger.error(f"Error al conectar con la base de datos: {str(e)}")
            return False