
from src.api.api import app
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen
from src.infraestructura.publicadores import PublicadorEventos
from src.infraestructura.suscriptores import SuscriptorEventos
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from src.seedwork.aplicacion.autenticacion import token_required
import logging
from src.infraestructura.gcp_storage import GCPStorage
from src.seedwork.infraestructura.utils import broker_host
from src.aplicacion.comandos.anonimizar_imagen import procesar_comando_ingesta
from src.aplicacion.comandos.rollback import rollback
from src.config.db import init_db, database_connection
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
            'comando_ingesta_imagenes',
            'anonimizacion-service-sub',
            procesar_comando_ingesta
        )

        suscriptor.suscribirse_a_topico(
            'comando_ingesta_imagenes_rollback',
            'anonimizacion-service-rollback-sub',
            rollback
        )

        logger.info("Suscriptor iniciado correctamente")
    except Exception as e:
        logger.error(f"Error al iniciar suscriptor: {str(e)}")

def inicializar_db(app):
    """Inicializa la base de datos y crea las tablas necesarias"""
    try:
        with app.app_context():
            logger.info("Creando tablas en la base de datos...")
            from src.infraestructura.dto import ImagenAnonimizada
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
    app.run(debug=True,port=5001)