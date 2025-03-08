import pulsar
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PublicadorEventos:
    def __init__(self, broker_url):
        self.client = pulsar.Client(broker_url)
    
    def publicar_evento(self, topico, mensaje):
        """
        Publica un mensaje en un tópico específico
        
        Args:
            topico: Nombre del tópico
            mensaje: Mensaje a publicar (se codificará como UTF-8)
        """
        try:
            producer = self.client.create_producer(topico)
            producer.send(mensaje.encode('utf-8'))
            producer.close()
            logger.info(f"Mensaje publicado en tópico {topico}")
        except Exception as e:
            logger.error(f"Error al publicar mensaje en tópico {topico}: {str(e)}")

    def cerrar(self):
        """Cierra la conexión con el broker"""
        self.client.close()
        logger.info("Conexión con Pulsar cerrada")