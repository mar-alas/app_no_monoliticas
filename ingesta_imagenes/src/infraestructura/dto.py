"""DTOs para la capa de infrastructura del dominio de ingesta

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de ingesta

"""

from src.config.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
from datetime import datetime
import uuid

class IngestaImagenes(db.Model):
    __tablename__ = "ingesta_imagenes"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    filename = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    binario_url = db.Column(db.String, nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    proveedor = db.Column(db.String, nullable=False)