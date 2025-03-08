import pulsar
from src.aplicacion.queries.ingestar_imagen import ObtenerIngestaHandler, ObtenerIngesta
import json
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PulsarSubscriber:
    def __init__(self, service_url: str, topic: str, subscription_name: str):
        self.client = pulsar.Client(service_url)
        self.topic = topic
        self.subscription_name = subscription_name

    def subscribe(self, callback):
        consumer = self.client.subscribe(self.topic, self.subscription_name)
        while True:
            msg = consumer.receive()
            try:
                callback(msg.value())
                consumer.acknowledge(msg)
            except Exception as e:
                consumer.negative_acknowledge(msg)
                print(f"Failed to process message: {e}")

    def _deserialize_message(self, data: bytes) -> ObtenerIngesta:
        message_dict = json.loads(data)
        return ObtenerIngesta(**message_dict)

    def close(self):
        self.client.close()

class SuscriptorEventos:
    def __init__(self, broker_url):
        self.client = pulsar.Client(broker_url)
        self.consumidores = []
        self.hilos = []
    
    def suscribirse_a_topico(self, topico, subscripcion, callback,avro_schema):
        """
        Suscribe a un tópico específico de Pulsar
        
        Args:
            topico: Nombre del tópico
            subscripcion: Nombre de la subscripción
            callback: Función a ejecutar cuando se recibe un mensaje
        """
        consumer = self.client.subscribe(
            topico,
            subscription_name=subscripcion,
            consumer_type=pulsar.ConsumerType.Shared,
            schema=avro_schema
        )
        
        self.consumidores.append(consumer)
        
        # Crear un hilo para consumir mensajes
        hilo = threading.Thread(target=self._consumir_mensajes, args=(consumer, callback))
        hilo.daemon = True
        self.hilos.append(hilo)
        hilo.start()
        
        logger.info(f"Suscrito al tópico {topico} con subscripción {subscripcion}")
        
    def _consumir_mensajes(self, consumer, callback):
        """Consume mensajes de un tópico específico"""
        while True:
            try:
                mensaje = consumer.receive()
                # When using AvroSchema, the value() method returns the deserialized object
                datos_evento = mensaje.value()
                
                # Convert the Avro object to a dictionary
                datos_dict = datos_evento.__dict__
                
                # Ejecuta el callback con los datos recibidos
                callback(datos_dict)
                
                # Confirmar que se procesó el mensaje
                consumer.acknowledge(mensaje)
                
            except Exception as e:
                logger.error(f"Error al consumir mensaje: {str(e)}")
    
    def cerrar(self):
        """Cierra las conexiones al broker"""
        for consumidor in self.consumidores:
            consumidor.close()
        self.client.close()
        logger.info("Conexión con Pulsar cerrada")

