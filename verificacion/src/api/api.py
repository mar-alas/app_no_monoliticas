from flask import Blueprint, jsonify, request
import logging
from src.infraestructura.repositorios import RepositorioVerificacionesSQLAlchemy
from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Blueprint('verificacion_api', __name__)

@app.route('/')
def home():
    return jsonify(message="Microservicio de verificación de anonimización")

@app.route('/verificacion/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/verificacion/estado', methods=['GET'])
def estado():
    # Prueba  conexión a la base de datos
    repo = RepositorioVerificacionesSQLAlchemy()
    db_connection = repo.test_conexion()
    
    return jsonify({
        "servicio": "verificacion_anonimizacion",
        "estado": "activo",
        "version": "1.0.0",
        "base_datos": "conectada" if db_connection else "desconectada"
    }), 200

@app.route('/verificacion/estadisticas', methods=['GET'])
def estadisticas():
    """Endpoint para obtener estadísticas de verificaciones"""
    try:
        repo = RepositorioVerificacionesSQLAlchemy()
        stats = repo.obtener_estadisticas()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}")
        return jsonify({"error": "Error al obtener estadísticas"}), 500

@app.route('/verificacion/imagen/<id_imagen>', methods=['GET'])
def verificaciones_por_imagen(id_imagen):
    """Endpoint para obtener las verificaciones de una imagen específica"""
    try:
        repo = RepositorioVerificacionesSQLAlchemy()
        verificaciones = repo.obtener_por_imagen(id_imagen)
        
        # Serializar resultados
        resultados = []
        for verificacion in verificaciones:
            resultados.append({
                "id": verificacion.id,
                "id_imagen": verificacion.id_imagen,
                "nombre_imagen": verificacion.nombre_imagen,
                "resultado": verificacion.resultado,
                "detalle": verificacion.detalle,
                "fecha_verificacion": verificacion.fecha_verificacion.isoformat(),
                "proveedor": verificacion.proveedor
            })
        
        return jsonify(resultados), 200
    except Exception as e:
        logger.error(f"Error al obtener verificaciones para la imagen {id_imagen}: {str(e)}")
        return jsonify({"error": f"Error al obtener verificaciones para la imagen {id_imagen}"}), 500

@app.route('/verificacion/todas', methods=['GET'])
def todas_las_verificaciones():
    """Endpoint para obtener todas las verificaciones"""
    try:
        repo = RepositorioVerificacionesSQLAlchemy()
        verificaciones = repo.obtener_todas_serializadas()
        return jsonify(verificaciones), 200
    except Exception as e:
        logger.error(f"Error al obtener todas las verificaciones: {str(e)}")
        return jsonify({"error": "Error al obtener todas las verificaciones"}), 500

@app.route('/verificacion/solicitar', methods=['POST'])
def solicitar_verificacion():
    """Endpoint para solicitar una verificación manual"""
    try:
        datos = request.json
        
        if not datos or 'id_imagen' not in datos or 'filename' not in datos:
            return jsonify({"error": "Datos incompletos. Se requiere id_imagen y filename"}), 400
        
        id_imagen = datos.get('id_imagen')
        filename = datos.get('filename')
        proveedor = datos.get('proveedor', 'lat')
        
        # Llamar al servicio de verificación
        resultado = servicio_verificar_anonimizacion(id_imagen, filename, proveedor)
        
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Error al procesar la verificación"}), 500
            
    except Exception as e:
        logger.error(f"Error al solicitar verificación: {str(e)}")
        return jsonify({"error": "Error al solicitar verificación"}), 500