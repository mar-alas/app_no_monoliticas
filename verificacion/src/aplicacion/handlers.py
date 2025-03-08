import logging
import json
import uuid
from datetime import datetime

from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion
from src.seedwork.dominio.eventos import EventoDominio
from src.infraestructura.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import VerificacionResultadoPayload
from src.infraestructura.eventos_utils import RastreadorEventos, MedidorTiempo

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
        # Iniciar medidor de tiempo
        medidor = MedidorTiempo("procesamiento_evento_anonimizacion").iniciar()
        
        # Registrar evento recibido
        evento_id = RastreadorEventos.registrar_evento_recibido(evento, 'eventos-anonimizador')
        
        try:
            logger.info(f"Procesando evento de imagen anonimizada: {evento_id}")
            
            # Extraer datos necesarios del evento
            logger.info(f"Datos del evento: {evento.keys()}")
            if 'data' in evento:
                logger.info(f"Datos del evento: {evento['data']}")
                payload = evento['data']
                id_imagen = payload.id_imagen
                filename = payload.filename
                size = payload.size
                
                if not id_imagen:
                    logger.warning("Evento recibido con datos incompletos, falta id_imagen")
                    RastreadorEventos.registrar_evento_procesado(evento_id, 'FALLIDO_DATOS_INCOMPLETOS')
                    return
                if not filename:
                    logger.warning("Evento recibido con datos incompletos, falta el filename")
                    RastreadorEventos.registrar_evento_procesado(evento_id, 'FALLIDO_DATOS_INCOMPLETOS')
                    return

                # Asumimos proveedor 'lat' por defecto
                proveedor = "lat"
                
                # Llamar al servicio de verificación
                logger.info(f"Invocando servicio de verificación para {id_imagen}_{filename}")
                resultado_verificacion = servicio_verificar_anonimizacion(id_imagen, filename, proveedor)
                
                # Si el servicio devuelve un resultado, publicar un evento con ese resultado
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
                    
                    # Registrar evento enviado
                    RastreadorEventos.registrar_evento_enviado(
                        evento_id, 
                        'eventos-verificacion', 
                        'VerificacionCompletada'
                    )
                    
                    logger.info(f"Evento de resultado de verificación publicado para imagen {id_imagen}_{filename}")
                    
                    if resultado_verificacion["resultado"] == "APROBADA":
                        #TODO emitir evento de fin de saga
                        ...

                    # Registrar evento procesado exitosamente
                    medidor.detener()
                    RastreadorEventos.registrar_evento_procesado(
                        evento_id, 
                        'EXITOSO', 
                        medidor.duracion_ms()
                    )
                else:
                    logger.error(f"Error en el servicio de verificación para {id_imagen}_{filename}")
                    medidor.detener()
                    RastreadorEventos.registrar_evento_procesado(
                        evento_id, 
                        'FALLIDO_SERVICIO', 
                        medidor.duracion_ms()
                    )
            else:
                logger.warning("Evento recibido sin datos esperados")
                medidor.detener()
                RastreadorEventos.registrar_evento_procesado(
                    evento_id, 
                    'FALLIDO_FORMATO_INCORRECTO', 
                    medidor.duracion_ms()
                )
                
        except Exception as e:
            logger.error(f"Error procesando evento de imagen anonimizada: {str(e)}")
            medidor.detener()
            RastreadorEventos.registrar_evento_procesado(
                evento_id, 
                f'FALLIDO_EXCEPCION: {type(e).__name__}', 
                medidor.duracion_ms()
            )