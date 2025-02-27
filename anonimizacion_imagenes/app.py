from src.api.api import app
from src.infraestructura.publicadores import PublicadorEventos
from src.infraestructura.suscriptores import SuscriptorEventos
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from src.seedwork.aplicacion.autenticacion import token_required
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancia global del suscriptor
suscriptor = None

def procesar_comando_ingesta(mensaje):
    """
    Procesa los comandos de ingesta de imágenes recibidos del tópico
    
    Args:
        mensaje: Diccionario con la información del comando
    """
    try:
        logger.info(f"Comando de ingesta recibido: {mensaje}")
        # Aquí se implementaría la lógica para procesar el comando
        # Por ejemplo: descargar la imagen desde una URL, validarla, etc.
    except Exception as e:
        logger.error(f"Error procesando comando de ingesta: {str(e)}")


def iniciar_suscriptor():
    """Inicializa y configura el suscriptor de eventos"""
    global suscriptor
    try:
        logger.info("Iniciando suscriptor de eventos...")
        suscriptor = SuscriptorEventos('pulsar://localhost:6650')
        
        # Suscribirse al tópico comando_ingesta_imagenes
        suscriptor.suscribirse_a_topico(
            'comando_ingesta_imagenes',
            'anonimizacion-service-sub',
            procesar_comando_ingesta
        )
        logger.info("Suscriptor iniciado correctamente")
    except Exception as e:
        logger.error(f"Error al iniciar suscriptor: {str(e)}")

if __name__ == "__main__":
    iniciar_suscriptor()
    app.run(debug=True,port=5001)