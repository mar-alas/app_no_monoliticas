import os
import logging
import threading
from flask import Flask
from src.api.api import app as api_app
from src.config.db import init_db
from src.infraestructura.consumidores import SuscriptorEventos
from src.aplicacion.handlers import HandlerVerificacionIntegracion
from src.infraestructura.dto import Base
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración base de datos
    DB_USERNAME = os.getenv('DB_USERNAME', default="user")
    DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
    DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
    DB_PORT = os.getenv('DB_PORT', default="9003")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/verificacion_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar la base de datos
    logger.info("Inicializando la base de datos...")
    init_db(app)
    
    # Crear tablas si no existen
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Base.metadata.create_all(engine)
        logger.info("Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"Error al crear tablas: {str(e)}")
    
    # Registrar el blueprint de API
    app.register_blueprint(api_app)
    logger.info("API registrada exitosamente")
    
    return app

def suscribir_a_eventos():
    """Suscribe a los eventos del broker"""
    try:
        broker_host = os.getenv('BROKER_HOST', 'localhost')
        broker_url = f'pulsar://{broker_host}:6650'
        
        logger.info(f"Conectando al broker en: {broker_url}")
        suscriptor = SuscriptorEventos(broker_url)
        
        # Suscribirse al tópico de eventos de anonimización
        suscriptor.suscribirse_a_topico(
            'eventos-anonimizador',
            'sub-verificacion',
            HandlerVerificacionIntegracion.handle_imagen_anonimizada
        )
        
        logger.info("Suscrito a eventos de anonimización correctamente")
        
    except Exception as e:
        logger.error(f"Error al suscribirse a eventos: {str(e)}")
        # Reintentar después de un tiempo
        import time
        time.sleep(10)
        suscribir_a_eventos()

if __name__ == '__main__':
    # Crear e inicializar la aplicación
    app = create_app()
    logger.info("Aplicación inicializada correctamente")
    
    # Suscripción a eventos en un hilo separado
    logger.info("Iniciando suscripción a eventos...")
    thread = threading.Thread(target=suscribir_a_eventos)
    thread.daemon = True
    thread.start()
    
    # Iniciar la aplicación Flask
    logger.info("Iniciando servidor web...")
    puerto = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=puerto, debug=False)