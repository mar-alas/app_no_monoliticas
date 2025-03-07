from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9002")

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/ingesta_db'
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