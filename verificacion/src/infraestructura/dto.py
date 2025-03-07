"""DTOs para la capa de infraestructura del dominio de verificación

En este archivo se encuentran los DTOs (modelos anémicos) de la
infraestructura de verificación de anonimización de imágenes
"""
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, func, Text
from sqlalchemy.ext.declarative import declarative_base
import uuid
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import os

# Conexión a la base de datos
DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9003")
DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/verificacion_db'

Base = declarative_base()

class DTOVerificacion(Base):
    """DTO para la entidad de verificación"""
    __tablename__ = "verificacion"
    
    id = Column(String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_imagen = Column(String(40), nullable=False)
    nombre_imagen = Column(String(255), nullable=False)
    resultado = Column(String(20), nullable=False)  # APROBADA, RECHAZADA, ERROR
    detalle = Column(Text, nullable=True)
    fecha_verificacion = Column(DateTime, nullable=False, default=func.current_timestamp())
    proveedor = Column(String(40), nullable=False, default="lat")
    
    def __repr__(self):
        return f"<Verificacion(id='{self.id}', id_imagen='{self.id_imagen}', resultado='{self.resultado}')>"

class DTOVerificacionSchema(SQLAlchemyAutoSchema):
    """Schema para serializar/deserializar DTOVerificacion"""
    class Meta:
        model = DTOVerificacion
        include_relationships = True
        load_instance = True