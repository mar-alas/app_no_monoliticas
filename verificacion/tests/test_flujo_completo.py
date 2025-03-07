import os
import sys
import json
import time
import uuid
import logging
import pulsar
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def esperar_segundos(segundos):
    """Espera un número de segundos, mostrando una cuenta regresiva"""
    for i in range(segundos, 0, -1):
        logger.info(f"Esperando {i} segundos...")
        time.sleep(1)

def test_flujo_completo():
    """
    Prueba el flujo completo del microservicio:
    1. Publica un evento de anonimización
    2. Espera a que el servicio lo procese
    3. Suscribe a eventos de verificación y verifica el resultado
    """
    try:
        # Configuración del broker
        broker_host = os.getenv('BROKER_HOST', 'localhost')
        broker_url = f'pulsar://{broker_host}:6650'
        logger.info(f"Conectando al broker en: {broker_url}")
        
        # Crear cliente Pulsar
        client = pulsar.Client(broker_url)
        
        # Generar IDs únicos para esta prueba
        test_id = str(uuid.uuid4())[:8]
        id_imagen = f"test-{test_id}"
        filename = "f9814db7-71f6-44ea-94a8-64b5082b7ac4_test_image.jpeg"
        
        logger.info(f"Iniciando prueba con ID {test_id}")
        logger.info(f"ID de imagen: {id_imagen}")
        logger.info(f"Nombre de archivo: {filename}")
        
        # 1. Publicar evento de anonimización
        logger.info("Paso 1: Publicando evento de anonimización")
        producer = client.create_producer('eventos-anonimizador')
        
        # Crear mensaje de anonimización
        mensaje = {
            'id': str(uuid.uuid4()),
            'time': int(time.time() * 1000),
            'data': {
                'id_imagen': id_imagen,
                'filename': filename,
                'size': '1024',
                'fecha_creacion': datetime.now().isoformat()
            }
        }
        
        # Enviar mensaje
        producer.send(json.dumps(mensaje).encode('utf-8'))
        logger.info("Evento de anonimización enviado")
        producer.close()
        
        # 2. Esperar a que el servicio procese el evento
        logger.info("Paso 2: Esperando que el servicio procese el evento")
        esperar_segundos(5)
        
        # 3. Suscribirse a eventos de verificación
        logger.info("Paso 3: Suscribiéndose a eventos de verificación")
        verificacion_recibida = False
        
        def procesar_resultado(consumer, mensaje_recibido):
            nonlocal verificacion_recibida
            try:
                # Decodificar el mensaje
                datos = json.loads(mensaje_recibido.data().decode('utf-8'))
                
                # Verificar si corresponde a nuestra imagen de prueba
                if 'data' in datos and datos['data'].get('id_imagen') == id_imagen:
                    logger.info("¡Evento de verificación recibido para nuestra imagen de prueba!")
                    
                    # Mostrar detalles
                    resultado = datos['data'].get('resultado', 'DESCONOCIDO')
                    detalle = datos['data'].get('detalle', '')
                    logger.info(f"Resultado: {resultado}")
                    logger.info(f"Detalle: {detalle}")
                    
                    # Confirmar recepción
                    consumer.acknowledge(mensaje_recibido)
                    verificacion_recibida = True
                    return True
                else:
                    # No es nuestro evento, seguir buscando
                    consumer.acknowledge(mensaje_recibido)
                    return False
            except Exception as e:
                logger.error(f"Error procesando mensaje: {str(e)}")
                consumer.negative_acknowledge(mensaje_recibido)
                return False
        
        # Crear consumidor
        consumer = client.subscribe(
            'eventos-verificacion', 
            subscription_name=f'test-sub-{test_id}',
            consumer_type=pulsar.ConsumerType.Exclusive
        )
        
        # Esperar por el evento (con timeout)
        timeout = time.time() + 30  # 30 segundos de timeout
        while time.time() < timeout and not verificacion_recibida:
            try:
                # Recibir mensaje con timeout de 1 segundo
                mensaje = consumer.receive(timeout_millis=1000)
                if procesar_resultado(consumer, mensaje):
                    break
            except Exception as e:
                # Timeout o error, continuar esperando
                pass
        
        # Cerrar consumidor
        consumer.close()
        
        # Verificar resultado
        if verificacion_recibida:
            logger.info("✅ Prueba de flujo completo exitosa")
            return True
        else:
            logger.error("❌ Timeout esperando evento de verificación")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cerrar cliente
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    if test_flujo_completo():
        sys.exit(0)  # Éxito
    else:
        sys.exit(1)  # Error