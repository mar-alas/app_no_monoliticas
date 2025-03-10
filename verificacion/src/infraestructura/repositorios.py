import logging
from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os
from datetime import datetime

from src.infraestructura.dto import DTOVerificacion, DTOVerificacionSchema, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9003")

engine = create_engine(
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/verificacion_db',
    pool_size=5,
    max_overflow=2,
    pool_recycle=120,
    pool_timeout=30,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10}
)

class RepositorioVerificacionesSQLAlchemy:
    """Repositorio para el almacenamiento y consulta de verificaciones"""
    
    def __init__(self):
        Base.metadata.create_all(engine)
        self.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            self.Session.remove()

    def crear(self, verificacion: DTOVerificacion) -> DTOVerificacion:
        """
        Crea una nueva verificación en la base de datos
        
        Args:
            verificacion: DTO con la información de la verificación
            
        Returns:
            DTOVerificacion: La verificación creada
        """
        with self.session_scope() as session:
            session.add(verificacion)
            session.flush()
            logger.info(f"Verificación creada: {verificacion.id}")
            return verificacion

    def obtener_por_id(self, id_verificacion: str) -> DTOVerificacion:
        """
        Obtiene una verificación por su ID
        
        Args:
            id_verificacion: ID de la verificación
            
        Returns:
            DTOVerificacion: La verificación encontrada o None
        """
        with self.session_scope() as session:
            return session.query(DTOVerificacion).filter(DTOVerificacion.id == id_verificacion).first()

    def obtener_por_imagen(self, id_imagen: str) -> list:
        """
        Obtiene las verificaciones relacionadas con una imagen
        
        Args:
            id_imagen: ID de la imagen
            
        Returns:
            list: Lista de verificaciones relacionadas con la imagen
        """
        with self.session_scope() as session:
            return session.query(DTOVerificacion).filter(DTOVerificacion.id_imagen == id_imagen).all()

    def obtener_todas(self) -> list:
        """
        Obtiene todas las verificaciones
        
        Returns:
            list: Lista con todas las verificaciones
        """
        with self.session_scope() as session:
            return session.query(DTOVerificacion).all()

    def obtener_paginadas(self, pagina: int = 1, por_pagina: int = 10) -> tuple:
        """
        Obtiene verificaciones con paginación
        
        Args:
            pagina: Número de página
            por_pagina: Cantidad de elementos por página
            
        Returns:
            tuple: (verificaciones, total de registros)
        """
        with self.session_scope() as session:
            offset = (pagina - 1) * por_pagina
            verificaciones = session.query(DTOVerificacion).order_by(
                DTOVerificacion.fecha_verificacion.desc()
            ).offset(offset).limit(por_pagina).all()
            total = session.query(DTOVerificacion).count()
            return verificaciones, total

    def obtener_todas_serializadas(self) -> list:
        """
        Obtiene todas las verificaciones en formato serializable (dict)
        
        Returns:
            list: Lista con todas las verificaciones serializadas
        """
        verificaciones = self.obtener_todas()
        schema = DTOVerificacionSchema()
        return schema.dump(verificaciones, many=True)
    
    def contar_verificaciones(self) -> int:
        """
        Cuenta el total de verificaciones
        
        Returns:
            int: Total de verificaciones
        """
        with self.session_scope() as session:
            return session.query(DTOVerificacion).count()
    
    def contar_verificaciones_desde(self, fecha_inicio: datetime) -> int:
        """
        Cuenta las verificaciones desde una fecha
        
        Args:
            fecha_inicio: Fecha desde la cual contar
            
        Returns:
            int: Total de verificaciones desde la fecha
        """
        with self.session_scope() as session:
            return session.query(DTOVerificacion).filter(
                DTOVerificacion.fecha_verificacion >= fecha_inicio
            ).count()
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas sobre las verificaciones
        
        Returns:
            dict: Estadísticas de verificaciones
        """
        with self.session_scope() as session:
            total = session.query(DTOVerificacion).count()
            
            if total == 0:
                return {
                    "total": 0,
                    "aprobadas": 0,
                    "rechazadas": 0,
                    "porcentaje_aprobadas": 0,
                    "porcentaje_rechazadas": 0
                }
            
            aprobadas = session.query(DTOVerificacion).filter(DTOVerificacion.resultado == "APROBADA").count()
            rechazadas = session.query(DTOVerificacion).filter(DTOVerificacion.resultado == "RECHAZADA").count()
            
            return {
                "total": total,
                "aprobadas": aprobadas,
                "rechazadas": rechazadas,
                "porcentaje_aprobadas": round((aprobadas / total) * 100, 2) if total > 0 else 0,
                "porcentaje_rechazadas": round((rechazadas / total) * 100, 2) if total > 0 else 0
            }
    
    def obtener_estadisticas_periodo(self, fecha_inicio: datetime) -> dict:
        """
        Obtiene estadísticas sobre las verificaciones en un período
        
        Args:
            fecha_inicio: Fecha desde la cual obtener estadísticas
            
        Returns:
            dict: Estadísticas de verificaciones en el período
        """
        with self.session_scope() as session:
            total = session.query(DTOVerificacion).filter(
                DTOVerificacion.fecha_verificacion >= fecha_inicio
            ).count()
            
            if total == 0:
                return {
                    "total": 0,
                    "aprobadas": 0,
                    "rechazadas": 0,
                    "porcentaje_aprobadas": 0,
                    "porcentaje_rechazadas": 0,
                    "fecha_inicio": fecha_inicio.isoformat()
                }
            
            aprobadas = session.query(DTOVerificacion).filter(
                and_(
                    DTOVerificacion.fecha_verificacion >= fecha_inicio,
                    DTOVerificacion.resultado == "APROBADA"
                )
            ).count()
            
            rechazadas = session.query(DTOVerificacion).filter(
                and_(
                    DTOVerificacion.fecha_verificacion >= fecha_inicio,
                    DTOVerificacion.resultado == "RECHAZADA"
                )
            ).count()
            
            return {
                "total": total,
                "aprobadas": aprobadas,
                "rechazadas": rechazadas,
                "porcentaje_aprobadas": round((aprobadas / total) * 100, 2) if total > 0 else 0,
                "porcentaje_rechazadas": round((rechazadas / total) * 100, 2) if total > 0 else 0,
                "fecha_inicio": fecha_inicio.isoformat()
            }
    
    def obtener_ultimas_verificaciones(self, limite: int = 10) -> list:
        """
        Obtiene las últimas verificaciones ordenadas por fecha
        
        Args:
            limite: Cantidad máxima de verificaciones a retornar
            
        Returns:
            list: Lista con las últimas verificaciones
        """
        with self.session_scope() as session:
            return session.query(DTOVerificacion).order_by(
                DTOVerificacion.fecha_verificacion.desc()
            ).limit(limite).all()
    
    def test_conexion(self) -> bool:
        """
        Prueba la conexión a la base de datos
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            with engine.connect():
                return True
        except Exception as e:
            logger.error(f"Error al conectar con la base de datos: {str(e)}")
            return False