from flask import Blueprint, jsonify, request, make_response
import logging
from datetime import datetime, timedelta
import uuid

from src.infraestructura.repositorios import RepositorioVerificacionesSQLAlchemy
from src.aplicacion.servicio_verificacion import servicio_verificar_anonimizacion
from src.infraestructura.eventos_utils import RastreadorEventos, MedidorTiempo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Blueprint('verificacion_api', __name__)

# Medir tiempo de respuesta
@app.before_request
def before_request():
    request.start_time = datetime.now()

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        duration = datetime.now() - request.start_time
        response.headers.add('X-Response-Time', f"{duration.total_seconds() * 1000:.2f}ms")
    return response

@app.route('/')
def home():
    return jsonify(message="Microservicio de verificación de anonimización")

@app.route('/verificacion/ping', methods=['GET'])
def ping():
    return "pong", 200

@app.route('/verificacion/estado', methods=['GET'])
def estado():
    """Endpoint para verificar el estado del servicio"""
    medidor = MedidorTiempo("api_estado").iniciar()
    
    try:
        # Test conexión base de datos
        repo = RepositorioVerificacionesSQLAlchemy()
        db_connection = repo.test_conexion()
        
        # Contar verificaciones últimas 24 horas
        fecha_corte = datetime.now() - timedelta(days=1)
        verificaciones_recientes = repo.contar_verificaciones_desde(fecha_corte)
        
        resultado = {
            "servicio": "verificacion_anonimizacion",
            "estado": "activo",
            "version": "1.0.0",
            "base_datos": "conectada" if db_connection else "desconectada",
            "verificaciones_24h": verificaciones_recientes,
            "timestamp": datetime.now().isoformat()
        }
        
        medidor.detener().registrar()
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Error en endpoint de estado: {str(e)}")
        medidor.detener()
        return jsonify({"error": "Error al verificar estado"}), 500

# Endpoints verificaciones
@app.route('/verificacion/estadisticas', methods=['GET'])
def estadisticas():
    """Endpoint para obtener estadísticas de verificaciones"""
    medidor = MedidorTiempo("api_estadisticas").iniciar()
    
    try:
        repo = RepositorioVerificacionesSQLAlchemy()
        stats = repo.obtener_estadisticas()
        
        # Estadísticas por periodo
        # Último día
        fecha_ayer = datetime.now() - timedelta(days=1)
        stats_dia = repo.obtener_estadisticas_periodo(fecha_ayer)
        
        # Última semana
        fecha_semana = datetime.now() - timedelta(days=7)
        stats_semana = repo.obtener_estadisticas_periodo(fecha_semana)
        
        # Último mes
        fecha_mes = datetime.now() - timedelta(days=30)
        stats_mes = repo.obtener_estadisticas_periodo(fecha_mes)
        
        resultado = {
            "global": stats,
            "ultimo_dia": stats_dia,
            "ultima_semana": stats_semana,
            "ultimo_mes": stats_mes,
            "timestamp": datetime.now().isoformat()
        }
        
        medidor.detener().registrar()
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}")
        medidor.detener()
        return jsonify({"error": "Error al obtener estadísticas"}), 500

@app.route('/verificacion/imagen/<id_imagen>', methods=['GET'])
def verificaciones_por_imagen(id_imagen):
    """Endpoint para obtener las verificaciones de una imagen específica"""
    medidor = MedidorTiempo("api_verificaciones_imagen").iniciar()
    
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
        
        medidor.detener().registrar()
        return jsonify(resultados), 200
    except Exception as e:
        logger.error(f"Error al obtener verificaciones para la imagen {id_imagen}: {str(e)}")
        medidor.detener()
        return jsonify({"error": f"Error al obtener verificaciones para la imagen {id_imagen}"}), 500

@app.route('/verificacion/todas', methods=['GET'])
def todas_las_verificaciones():
    """Endpoint para obtener todas las verificaciones con paginación"""
    medidor = MedidorTiempo("api_todas_verificaciones").iniciar()
    
    try:
        # Parámetros de paginación
        pagina = request.args.get('pagina', default=1, type=int)
        por_pagina = request.args.get('por_pagina', default=10, type=int)
        
        # Limitar tamaño de página
        if por_pagina > 100:
            por_pagina = 100
        
        repo = RepositorioVerificacionesSQLAlchemy()
        verificaciones, total = repo.obtener_paginadas(pagina, por_pagina)
        
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
        
        # Construir respuesta con metadata de paginación
        respuesta = {
            "data": resultados,
            "meta": {
                "pagina_actual": pagina,
                "total_paginas": (total + por_pagina - 1) // por_pagina,
                "total_registros": total,
                "por_pagina": por_pagina
            }
        }
        
        medidor.detener().registrar()
        return jsonify(respuesta), 200
    except Exception as e:
        logger.error(f"Error al obtener todas las verificaciones: {str(e)}")
        medidor.detener()
        return jsonify({"error": "Error al obtener todas las verificaciones"}), 500

@app.route('/verificacion/<id_verificacion>', methods=['GET'])
def obtener_verificacion(id_verificacion):
    """Endpoint para obtener detalles de una verificación específica"""
    medidor = MedidorTiempo("api_verificacion_detalle").iniciar()
    
    try:
        repo = RepositorioVerificacionesSQLAlchemy()
        verificacion = repo.obtener_por_id(id_verificacion)
        
        if not verificacion:
            medidor.detener()
            return jsonify({"error": "Verificación no encontrada"}), 404
        
        resultado = {
            "id": verificacion.id,
            "id_imagen": verificacion.id_imagen,
            "nombre_imagen": verificacion.nombre_imagen,
            "resultado": verificacion.resultado,
            "detalle": verificacion.detalle,
            "fecha_verificacion": verificacion.fecha_verificacion.isoformat(),
            "proveedor": verificacion.proveedor
        }
        
        medidor.detener().registrar()
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Error al obtener verificación {id_verificacion}: {str(e)}")
        medidor.detener()
        return jsonify({"error": f"Error al obtener verificación {id_verificacion}"}), 500

# Endpoints para solicitudes de verificación
@app.route('/verificacion/solicitar', methods=['POST'])
def solicitar_verificacion():
    """Endpoint para solicitar una verificación manual"""
    medidor = MedidorTiempo("api_solicitar_verificacion").iniciar()
    
    try:
        datos = request.json
        
        if not datos or 'id_imagen' not in datos or 'filename' not in datos:
            medidor.detener()
            return jsonify({"error": "Datos incompletos. Se requiere id_imagen y filename"}), 400
        
        id_imagen = datos.get('id_imagen')
        filename = datos.get('filename')
        proveedor = datos.get('proveedor', 'lat')
        
        # Registrar evento de solicitud
        evento_id = str(uuid.uuid4())
        RastreadorEventos.registrar_evento_recibido(
            {'id': evento_id, 'data': datos}, 
            'api_solicitud_verificacion'
        )
        
        # Llamar al servicio de verificación
        resultado = servicio_verificar_anonimizacion(id_imagen, filename, proveedor)
        
        if resultado:
            # Registrar evento procesado
            RastreadorEventos.registrar_evento_procesado(
                evento_id, 
                'EXITOSO',
                medidor.detener().duracion_ms()
            )
            return jsonify(resultado), 200
        else:
            medidor.detener()
            return jsonify({"error": "Error al procesar la verificación"}), 500
            
    except Exception as e:
        logger.error(f"Error al solicitar verificación: {str(e)}")
        medidor.detener()
        return jsonify({"error": "Error al solicitar verificación"}), 500

# Endpoint de métricas para monitoreo
@app.route('/verificacion/metricas', methods=['GET'])
def metricas():
    """Endpoint para obtener métricas de rendimiento del servicio"""
    try:
        repo = RepositorioVerificacionesSQLAlchemy()
        
        # Obtener métricas básicas
        total_verificaciones = repo.contar_verificaciones()
        verificaciones_hoy = repo.contar_verificaciones_desde(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        
        resultado = {
            "total_verificaciones": total_verificaciones,
            "verificaciones_hoy": verificaciones_hoy,
            "uptime": "N/A",
            "memoria_usada": "N/A",
            "cpu_usada": "N/A",
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Error al obtener métricas: {str(e)}")
        return jsonify({"error": "Error al obtener métricas"}), 500