"""DTOs para la capa de infrastructura del dominio de ingesta

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de ingesta

"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f'sqlite:///' + os.path.join(basedir, 'ingesta.db')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class IngestaImagenes(Base):
    __tablename__ = "ingesta_imagenes"
    id = Column(String, primary_key=True)
    fecha_creacion = Column(DateTime, nullable=False)
    filename = Column(String, nullable=False)
    size = Column(String, nullable=False)
    binario_url = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    proveedor = Column(String, nullable=False)

Base.metadata.create_all(engine)