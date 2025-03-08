import pulsar
from src.aplicacion.queries.ingestar_imagen import ObtenerIngestaHandler, ObtenerIngesta
import json

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