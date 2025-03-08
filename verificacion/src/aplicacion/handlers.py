import logging
import json
import time
import uuid
from datetime import datetime

from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion
from src.seedwork.dominio.eventos import EventoDominio
from src.infraestructura.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import EventoIntegracionVerificacionCompletada,VerificacionResultadoPayload,FinSagaPayload,EventoIntegracionFinSaga
from src.infraestructura.schema.v1.comandos import ComandoAnonimizacionRollback
from src.infraestructura.eventos_utils import RastreadorEventos, MedidorTiempo
from pulsar.schema import AvroSchema

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
                    payload = VerificacionResultadoPayload(
                        id_verificacion=str(resultado_verificacion.get('id_verificacion')),
                        id_imagen=id_imagen,
                        filename=filename,
                        resultado=resultado_verificacion.get('resultado'),
                        detalle=resultado_verificacion.get('detalle', ''),
                        fecha_verificacion=resultado_verificacion.get('fecha_verificacion')
                    )

                    evento_integracion = EventoIntegracionVerificacionCompletada(
                        data=payload,
                        time=int(time.time() * 1000),
                        ingestion=0,
                        specversion="v1",
                        type="VerificacionCompletada",
                        datacontenttype="application/json",
                        service_name="verificacion_anonimizacion"
                    )
                    
                    avro_schema=AvroSchema(EventoIntegracionVerificacionCompletada)

                    
                    # Registrar evento enviado
                    RastreadorEventos.registrar_evento_enviado(
                        evento_id, 
                        'eventos-verificacion', 
                        'VerificacionCompletada'
                    )
                    
                    logger.info(f"Evento de resultado de verificación publicado para imagen {id_imagen}_{filename}")
                    logger.info(f"Resultado de la verificacion {resultado_verificacion['resultado']}")

                    if resultado_verificacion["resultado"] == "APROBADA":
                        evento_integracion.event_name="VerificacionExitosa"
                        despachador.publicar_evento(evento_integracion, 'eventos-verificacion',avro_schema)
                    
                        payload = FinSagaPayload(mensaje="Fin saga")
                        evento_integracion = EventoIntegracionFinSaga(data=payload)
                        avro_schema=AvroSchema(EventoIntegracionFinSaga)
                        despachador.publicar_evento(evento_integracion, 'eventos-fin-saga',avro_schema)
                    else:
                        evento_integracion.event_name="VerificacionFallida"
                        despachador.publicar_evento(evento_integracion, 'eventos-verificacion',avro_schema)

                        comando=ComandoAnonimizacionRollback()
                        avro_schema=AvroSchema(ComandoAnonimizacionRollback)
                        despachador.publicar_evento(comando, 'comando_anonimizacion_imagenes_rollback',avro_schema)

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