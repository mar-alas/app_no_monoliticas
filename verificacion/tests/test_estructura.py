import logging
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_estructura():
    """
    Prueba la estructura básica del proyecto verificando las importaciones
    """
    try:
        logger.info("Probando importaciones básicas...")
        
        # Probar importaciones de módulos principales
        from src.infraestructura.despachadores import Despachador
        from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion
        from src.infraestructura.repositorios import RepositorioVerificacionesSQLAlchemy
        from src.dominio.entidades import EntidadVerificacion
        
        logger.info("✅ Importaciones básicas exitosas")
        
        # Probar la creación de instancias
        despachador = Despachador()
        logger.info("✅ Creación de despachador exitosa")
        
        # Verificar variables de entorno
        broker_host = os.getenv('BROKER_HOST', 'localhost')
        logger.info(f"BROKER_HOST: {broker_host}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_estructura():
        logger.info("✅ Prueba de estructura exitosa")
        sys.exit(0)
    else:
        logger.error("❌ Prueba de estructura fallida")
        sys.exit(1)