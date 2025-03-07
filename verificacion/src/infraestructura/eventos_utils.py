import logging
import json
import time
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class RastreadorEventos:
    """
    Clase para rastrear eventos y sus metadatos a través del flujo del sistema
    """
    @staticmethod
    def registrar_evento_recibido(evento, topico):
        """
        Registra un evento recibido y sus metadatos
        
        Args:
            evento: Diccionario con la información del evento
            topico: Tópico del que se recibió el evento
        """
        try:
            evento_id = evento.get('id', str(uuid.uuid4()))
            timestamp = datetime.now().isoformat()
            
            logger.info(f"EVENTO_RECIBIDO|{evento_id}|{topico}|{timestamp}")
            
            # Almacenar metadatos adicionales con nivel DEBUG
            if 'data' in evento:
                data_resumen = {k: v for k, v in evento['data'].items() if k not in ['binario']}
                logger.debug(f"DETALLES_EVENTO|{evento_id}|{json.dumps(data_resumen)}")
                
            return evento_id
        except Exception as e:
            logger.error(f"Error al registrar evento recibido: {str(e)}")
            return None

    @staticmethod
    def registrar_evento_procesado(evento_id, resultado, duracion_ms=None):
        """
        Registra que un evento ha sido procesado y su resultado
        
        Args:
            evento_id: ID del evento
            resultado: Resultado del procesamiento ('EXITOSO', 'FALLIDO', etc.)
            duracion_ms: Duración del procesamiento en milisegundos
        """
        try:
            timestamp = datetime.now().isoformat()
            duracion_str = f"|{duracion_ms}ms" if duracion_ms is not None else ""
            
            logger.info(f"EVENTO_PROCESADO|{evento_id}|{resultado}|{timestamp}{duracion_str}")
        except Exception as e:
            logger.error(f"Error al registrar evento procesado: {str(e)}")

    @staticmethod
    def registrar_evento_enviado(evento_id, topico, tipo_evento):
        """
        Registra que un evento ha sido enviado
        
        Args:
            evento_id: ID del evento original
            topico: Tópico al que se envió el evento resultante
            tipo_evento: Tipo del evento enviado
        """
        try:
            timestamp = datetime.now().isoformat()
            
            logger.info(f"EVENTO_ENVIADO|{evento_id}|{topico}|{tipo_evento}|{timestamp}")
        except Exception as e:
            logger.error(f"Error al registrar evento enviado: {str(e)}")

class MedidorTiempo:
    """Clase para medir la duración de operaciones"""
    
    def __init__(self, nombre_operacion=None):
        self.nombre_operacion = nombre_operacion
        self.inicio = None
        self.fin = None
    
    def iniciar(self):
        """Inicia la medición de tiempo"""
        self.inicio = time.time()
        return self
    
    def detener(self):
        """Detiene la medición de tiempo"""
        self.fin = time.time()
        return self
    
    def duracion_ms(self):
        """Devuelve la duración en milisegundos"""
        if self.inicio is None or self.fin is None:
            return None
        return int((self.fin - self.inicio) * 1000)
    
    def registrar(self):
        """Registra la duración en los logs"""
        if self.nombre_operacion:
            duracion = self.duracion_ms()
            if duracion is not None:
                logger.info(f"DURACION|{self.nombre_operacion}|{duracion}ms")
            return duracion
        return None