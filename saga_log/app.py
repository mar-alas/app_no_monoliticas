from flask import Flask, jsonify
import os
from config import app
import logging
from dto import db, SagaLog,SagaLogSchema
from servicios import almacenar_saga_log
from eventos import EventoIntegracionImagenAnonimizada,EventoIntegracionImagenIngestada
from eventos import EventoIntegracionInicioSaga
from pulsar.schema import AvroSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Initialize SQLAlchemy with app
db.init_app(app)

def broker_host():
    return os.getenv('BROKER_HOST', 'localhost')



def iniciar_suscriptor():
    """Inicializa y configura el suscriptor de eventos"""
    from consumidores import SuscriptorEventos
    global suscriptor
    try:
        pulsar_host=broker_host()
        suscriptor = SuscriptorEventos(f'pulsar://{pulsar_host}:6650')
        
        
        suscriptor.suscribirse_a_topico(
            topico='eventos-bff',
            subscripcion='sagalog-sub',
            callback=almacenar_saga_log,
            avro_schema=AvroSchema(EventoIntegracionInicioSaga)
        )

        suscriptor.suscribirse_a_topico(
            topico='eventos-ingesta',
            subscripcion='sagalog-sub',
            callback=almacenar_saga_log,
            avro_schema=AvroSchema(EventoIntegracionImagenIngestada)
        )
        
        suscriptor.suscribirse_a_topico(
            topico='eventos-anonimizador',
            subscripcion='sagalog-sub',
            callback=almacenar_saga_log,
            avro_schema=AvroSchema(EventoIntegracionImagenAnonimizada)
        )

        

        logger.info("Suscriptor iniciado correctamente")
    except Exception as e:
        logger.error(f"Error al iniciar suscriptor: {str(e)}")


@app.route('/ping', methods=['GET'])
def home():
    return jsonify(message="pong!")

@app.route('/erase', methods=['GET'])
def erase():
    session=db.session
    SagaLog.query.delete()
    session.commit()
    session.close()
    return jsonify(message="Database tables erased successfully")

@app.route('/get-logs', methods=['GET'])
def query_logs():
    session=db.session
    logs=SagaLog.query.all()
    session.close()
    schema=SagaLogSchema(many=True)
    logs_json=schema.dump(logs)
    
    return jsonify(logs_json)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    iniciar_suscriptor()
    app.run(host="0.0.0.0",port=5003,debug=True)