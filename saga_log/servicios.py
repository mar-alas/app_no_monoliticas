from config import app
from dto import db, SagaLog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def almacenar_saga_log(mensaje: dict):
    with app.app_context():
        session = db.session
        event_name= mensaje["event_name"]
        sagalog = SagaLog(evento=str(event_name))
        session.add(sagalog)
        session.commit()
        session.close()

    logger.info(f"transaccion almacenada")

