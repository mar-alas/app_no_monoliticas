import os
import pulsar
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_broker_connection():
    """Prueba la conexión al broker de Pulsar"""
    try:
        # Obtener el host del broker desde las variables de entorno
        broker_host = os.getenv('BROKER_HOST', 'localhost')
        broker_url = f'pulsar://{broker_host}:6650'
        
        logger.info(f"Conectando al broker en: {broker_url}")
        
        # Crear un cliente Pulsar
        client = pulsar.Client(broker_url)
        
        # Crear un productor de prueba
        producer = client.create_producer('test-topic')
        
        # Publicar un mensaje de prueba
        producer.send("Mensaje de prueba de conexión".encode('utf-8'))
        logger.info("Mensaje de prueba enviado correctamente")
        
        # Cerrar las conexiones
        producer.close()
        client.close()
        logger.info("Conexión con el broker exitosa y cerrada correctamente")
        
        return True
    except Exception as e:
        logger.error(f"Error conectando al broker: {str(e)}")
        return False

if __name__ == "__main__":
    if test_broker_connection():
        logger.info("✅ La prueba de conexión al broker fue exitosa")
    else:
        logger.error("❌ La prueba de conexión al broker falló")