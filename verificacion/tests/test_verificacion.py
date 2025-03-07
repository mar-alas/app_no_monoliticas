import logging
import sys
import uuid
from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_servicio_verificacion():
    """
    Prueba el servicio de verificación con un caso de prueba básico
    """
    try:
        # Valores de prueba
        id_imagen = str(uuid.uuid4())
        filename = "test_image.jpg"
        proveedor = "lat"
        
        logger.info(f"Probando servicio de verificación con id_imagen={id_imagen}, filename={filename}")
        
        # Llamar al servicio de verificación
        # Simular decisión aleatoria
        resultado = servicio_verificar_anonimizacion(id_imagen, filename, proveedor)
        
        if resultado:
            logger.info(f"Resultado de verificación: {resultado}")
            logger.info("✅ Prueba exitosa")
            return True
        else:
            logger.error("❌ La prueba falló - El servicio no devolvió un resultado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    # Realizar prueba y devolver el código de estado
    if test_servicio_verificacion():
        sys.exit(0)  # Éxito
    else:
        sys.exit(1)  # Error