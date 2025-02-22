import pulsar

class PublicadorEventos:
    def __init__(self, broker_url):
        self.client = pulsar.Client(broker_url)
    
    def publicar_evento(self, topico, mensaje):
        producer = self.client.create_producer(topico)
        producer.send(mensaje.encode('utf-8'))
        producer.close()

    def cerrar(self):
        self.client.close()