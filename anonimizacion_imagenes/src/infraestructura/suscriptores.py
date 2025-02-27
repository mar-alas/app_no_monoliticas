import pulsar
import threading
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SuscriptorEventos:
    def __init__(self, broker_url):
        self.client = pulsar.Client(broker_url)
        self.consumidores = []
        self.hilos = []
    
    def suscribirse_a_topico(self, topico, subscripcion, callback):
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
            consumer_type=pulsar.ConsumerType.Shared
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
                datos = mensaje.data().decode('utf-8')
                
                # Intenta procesar el mensaje como JSON
                try:
                    datos_dict = json.loads(datos)
                except json.JSONDecodeError:
                    datos_dict = {"mensaje": datos}
                
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