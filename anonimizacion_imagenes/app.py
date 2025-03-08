

from src.api.api import app

#si se borran estos paquetes causan conflicto al correr app
#import cv2
#import easyocr
import numpy as np


from src.infraestructura.publicadores import PublicadorEventos
from src.infraestructura.consumidores import SuscriptorEventos
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from src.seedwork.aplicacion.autenticacion import token_required
import logging
from src.infraestructura.gcp_storage import GCPStorage
from src.seedwork.infraestructura.utils import broker_host
from src.config.db import init_db, database_connection
from src.aplicacion.comandos.anonimizar_imagen import procesar_comando_anonimizacion
from src.aplicacion.comandos.rollback import rollback
from src.infraestructura.schema.v1.comandos import ComandoAnonimizarImagen, ComandoAnonimizacionRollback
from pulsar.schema import AvroSchema
import os
import psycopg2

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancia global del suscriptor
suscriptor = None


def iniciar_suscriptor():
    """Inicializa y configura el suscriptor de eventos"""
    global suscriptor
    try:
        pulsar_host=broker_host()
        suscriptor = SuscriptorEventos(f'pulsar://{pulsar_host}:6650')
        
        suscriptor.suscribirse_a_topico(
            'comando_anonimizacion_imagenes',
            'anonimizacion-service-sub',
            procesar_comando_anonimizacion,
            avro_schema=AvroSchema(ComandoAnonimizarImagen)
        )

        suscriptor.suscribirse_a_topico(
            'comando_anonimizacion_imagenes_rollback',
            'anonimizacion-service-rollback-sub',
            rollback,
            avro_schema=AvroSchema(ComandoAnonimizacionRollback)
        )

        logger.info("Suscriptor iniciado correctamente")
    except Exception as e:
        logger.error(f"Error al iniciar suscriptor: {str(e)}")

def inicializar_db(app):
    """Inicializa la base de datos y crea las tablas necesarias"""
    try:
        with app.app_context():
            logger.info("Creando tablas en la base de datos...")
            from src.infraestructura.dto import DTOImagenAnonimizada
            from src.config.db import db
            db.create_all()
            logger.info("Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"Error al crear tablas en la base de datos: {str(e)}")


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection({}, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    inicializar_db(app)
    iniciar_suscriptor()
    app.run(host="0.0.0.0",port=5001,debug=True)