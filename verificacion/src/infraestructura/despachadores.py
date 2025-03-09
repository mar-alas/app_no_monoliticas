import pulsar
from pulsar.schema import *
import logging
import time
import os
from datetime import datetime

from src.infraestructura.schema.v1.eventos import EventoIntegracionVerificacionCompletada, VerificacionResultadoPayload
from src.infraestructura.eventos_utils import RastreadorEventos, MedidorTiempo
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función de utilidad local
def broker_host():
    return os.getenv('BROKER_HOST', 'localhost')

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        """
        Publica un mensaje en un tópico específico
        
        Args:
            mensaje: Mensaje a publicar
            topico: Tópico donde publicar
            schema: Esquema del mensaje
        """
        medidor = MedidorTiempo(f"publicacion_mensaje_{topico}").iniciar()
        
        try:
            # Crear cliente y productor
            cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
            publicador = cliente.create_producer(topico, schema=schema)
            
            # Publicar mensaje
            publicador.send(mensaje)
            logger.info(f"Mensaje publicado exitosamente en tópico {topico}")
            
            # Cerrar conexiones
            publicador.close()
            cliente.close()
            
            medidor.detener().registrar()
            
        except Exception as e:
            logger.error(f"Error al publicar mensaje en tópico {topico}: {str(e)}")
            medidor.detener()
            raise

    def publicar_evento(self, evento: EventoIntegracion, topico,avro_schema):
        """
        Publica un evento de verificación en el tópico especificado
        
        Args:
            evento: evento de integracion
            topico: Tópico donde publicar
        """
        try:
            # Crear evento de integración
            evento_integracion = evento
            
            # Publicar el mensaje
            self._publicar_mensaje(evento_integracion, topico, avro_schema)
            
            # Registrar el envío del evento
            logger.info(f"Evento {evento_integracion.id} publicado en tópico {topico}")
            
            return evento_integracion.id
            
        except Exception as e:
            logger.error(f"Error al publicar evento: {str(e)}")
            return None