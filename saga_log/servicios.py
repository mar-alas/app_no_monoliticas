from config import app
from dto import db, SagaLog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def almacenar_saga_log(mensaje: dict):
    with app.app_context():
        session = db.session
        event_name= mensaje["event_name"]
        logger.info(f"almacenando transaccion {str(mensaje)}")
        try:
            id_correlacion=mensaje["id_correlacion"]
        except:
            id_correlacion="sin_asignar"

        sagalog = SagaLog(evento=str(event_name),id_correlacion=id_correlacion)
        session.add(sagalog)
        session.commit()
        session.close()

    logger.info(f"transaccion almacenada")

