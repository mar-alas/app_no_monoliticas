"""DTOs para la capa de infrastructura del dominio de imagenes anonimizadas

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura de la anonimizacion de imagenes

"""
from src.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
import uuid

Base = db.declarative_base()

class ImagenAnonimizada(db.Model):
    __tablename__ = "imagen_anonimizada"
    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    fileName = db.Column(db.String(40), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())