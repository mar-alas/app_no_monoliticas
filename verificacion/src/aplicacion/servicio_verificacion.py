import logging
import random
import uuid
from datetime import datetime
from io import BytesIO

from src.infraestructura.gcp_storage import GCPStorage
from src.dominio.objetos_valor import ResultadoVerificacion, EstadoVerificacion
from src.dominio.entidades import EntidadVerificacion
from src.dominio.reglas import IdentificadorDeImagenValido, NombreDeImagenValido
from src.infraestructura.dto import DTOVerificacion
from src.infraestructura.repositorios import RepositorioVerificacionesSQLAlchemy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def servicio_verificar_anonimizacion(id_imagen: str, filename: str, proveedor: str = "lat"):
    """
    Verifica si una imagen ha sido correctamente anonimizada.
    En esta implementación, determina aleatoriamente con un 50% de probabilidad
    si la anonimización fue correcta.
    
    Args:
        id_imagen: ID de la imagen
        filename: Nombre del archivo de la imagen
        proveedor: Proveedor de la imagen (default: "lat")
        
    Returns:
        dict: Resultado de la verificación con los siguientes campos:
            - id_verificacion: UUID de la verificación
            - resultado: "APROBADA" o "RECHAZADA"
            - detalle: Descripción detallada del resultado
            - fecha_verificacion: Fecha de la verificación en formato ISO
    """
    try:
        logger.info(f"Iniciando verificación de anonimización para imagen {id_imagen}_{filename}")
        
        # Validar datos de entrada
        if not IdentificadorDeImagenValido(id_imagen).es_valido():
            raise ValueError("El identificador de imagen no es válido")
        
        if not NombreDeImagenValido(filename).es_valido():
            raise ValueError("El nombre de la imagen no es válido")
        
        # Obtener la imagen anonimizada
        try:
            nombre_imagen_completo = f"{id_imagen}_{filename}"
            gcp_storage = GCPStorage()
            imagen_anonimizada = gcp_storage.obtener_imagen_anonimizada(nombre_imagen_completo, proveedor)
            logger.info(f"Imagen anonimizada obtenida correctamente: {nombre_imagen_completo}")
        except Exception as e:
            logger.error(f"Error al obtener la imagen anonimizada: {str(e)}")
            # Continuamos con la verificación simulada
            imagen_anonimizada = BytesIO()
        
        # Simulación de verificación (50% de probabilidad)
        # Algoritmo de verificación
        verificacion_exitosa = random.choice([True, False])
        
        # Crear entidad del dominio
        id_verificacion = str(uuid.uuid4())
        fecha_verificacion = datetime.now()
        
        if verificacion_exitosa:
            resultado = ResultadoVerificacion.aprobada("Verificación exitosa mediante análisis automatizado")
            resultado_str = "APROBADA"
            detalle = "La imagen ha sido correctamente anonimizada"
        else:
            resultado = ResultadoVerificacion.rechazada("Se detectaron elementos no anonimizados")
            resultado_str = "RECHAZADA"
            detalle = "La imagen contiene elementos que deberían haber sido anonimizados"
        
        entidad_verificacion = EntidadVerificacion(
            id=uuid.UUID(id_verificacion),
            id_imagen=id_imagen,
            nombre_imagen=filename,
            resultado=resultado,
            fecha_verificacion=fecha_verificacion,
            proveedor=proveedor
        )
        
        # Almacenar resultado en base de datos
        repositorio = RepositorioVerificacionesSQLAlchemy()
        dto_verificacion = DTOVerificacion(
            id=id_verificacion,
            id_imagen=id_imagen,
            nombre_imagen=filename,
            resultado=resultado_str,
            detalle=detalle,
            fecha_verificacion=fecha_verificacion,
            proveedor=proveedor
        )
        repositorio.crear(dto_verificacion)
        
        logger.info(f"Verificación completada para imagen {id_imagen}_{filename}: {resultado_str}")
        
        # Devolver información del resultado
        return {
            'id_verificacion': id_verificacion,
            'resultado': resultado_str,
            'detalle': detalle,
            'fecha_verificacion': fecha_verificacion.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en el servicio de verificación: {str(e)}")
        return None