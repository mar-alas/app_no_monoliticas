import logging
from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HandlerVerificacionIntegracion:
    @staticmethod
    def handle_imagen_anonimizada(evento):
        """
        Maneja los eventos de imágenes anonimizadas recibidos del tópico
        
        Args:
            evento: Diccionario con la información del evento
        """
        try:
            logger.info(f"Evento de imagen anonimizada recibido: {evento}")
            
            # Extraer datos necesarios del evento
            if 'data' in evento:
                datos = evento['data']
                id_imagen = datos.get('id_imagen')
                filename = datos.get('filename')
                
                # Llamar al servicio de verificación
                servicio_verificar_anonimizacion(id_imagen, filename)
            else:
                logger.warning("Evento recibido sin datos esperados")
                
        except Exception as e:
            logger.error(f"Error procesando evento de imagen anonimizada: {str(e)}")