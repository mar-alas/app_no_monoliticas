"""DTOs para la capa de infrastructura del dominio de imagenes anonimizadas

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura de la anonimizacion de imagenes

"""
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, func,Integer
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# Define the database connection
DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9001")
DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/anonimizacion_db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class DTOImagenAnonimizada(Base):
    __tablename__ = "imagen_anonimizada"
    id = Column(String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_imagen_origen = Column(String(80), nullable=False)
    nombre_imagen_destino = Column(String(80), nullable=False)
    tamanio_archivo=Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False, default=func.current_timestamp())

class DTOImagenAnonimizadaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DTOImagenAnonimizada

Base.metadata.create_all(engine)