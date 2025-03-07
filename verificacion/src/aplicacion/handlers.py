import logging
from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion
from src.seedwork.dominio.eventos import EventoDominio
from src.infraestructura.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import VerificacionResultadoPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler:
    """Clase base para los handlers"""
    
    @staticmethod
    def handle_event(evento):
        raise NotImplementedError

class HandlerVerificacionIntegracion(Handler):
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
                size = datos.get('size', '0')
                
                if not id_imagen or not filename:
                    logger.warning("Evento recibido con datos incompletos, falta id_imagen o filename")
                    return
                
                # Proveedor 'lat' por defecto
                proveedor = "lat"
                
                # Llamar al servicio de verificación
                resultado_verificacion = servicio_verificar_anonimizacion(id_imagen, filename, proveedor)
                
                # Si el servicio devuelve un resultado, publicar evento
                if resultado_verificacion:
                    despachador = Despachador()
                    
                    # Crear payload del evento
                    resultado_evento = VerificacionResultadoPayload(
                        id_verificacion=str(resultado_verificacion.get('id_verificacion')),
                        id_imagen=id_imagen,
                        filename=filename,
                        resultado=resultado_verificacion.get('resultado'),
                        detalle=resultado_verificacion.get('detalle', ''),
                        fecha_verificacion=resultado_verificacion.get('fecha_verificacion')
                    )
                    
                    # Publicar evento
                    despachador.publicar_evento(resultado_evento, 'eventos-verificacion')
                    logger.info(f"Evento de resultado de verificación publicado para imagen {id_imagen}_{filename}")
            else:
                logger.warning("Evento recibido sin datos esperados")
                
        except Exception as e:
            logger.error(f"Error procesando evento de imagen anonimizada: {str(e)}")