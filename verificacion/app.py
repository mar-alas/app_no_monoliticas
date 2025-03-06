import os
import logging
from flask import Flask
from src.api.api import app as api_app
from src.config.db import init_db
from src.infraestructura.consumidores import SuscriptorEventos
from src.aplicacion.handlers import HandlerVerificacionIntegracion

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://user:password@{os.getenv("DB_HOSTNAME", "localhost")}:{os.getenv("DB_PORT", "5432")}/verificacion_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar la base de datos
    init_db(app)
    
    # Registrar el blueprint de API
    app.register_blueprint(api_app)
    
    return app

def suscribir_a_eventos():
    """Suscribe a los eventos del broker"""
    try:
        broker_host = os.getenv('BROKER_HOST', 'localhost')
        broker_url = f'pulsar://{broker_host}:6650'
        
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

if __name__ == '__main__':
    app = create_app()
    
    # Iniciar la suscripción a eventos en un hilo separado
    import threading
    thread = threading.Thread(target=suscribir_a_eventos)
    thread.daemon = True
    thread.start()
    
    # Iniciar la aplicación Flask
    app.run(host='0.0.0.0', port=5002, debug=True)