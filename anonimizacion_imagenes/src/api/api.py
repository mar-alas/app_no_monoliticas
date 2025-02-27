#this runs with python3 src/api/api.py from microservice root folder

from io import BytesIO
from flask import Flask, jsonify, request, send_file
from src.aplicacion.servicio_anonimizar import servicio_anonimizar_imagen
from src.infraestructura.publicadores import PublicadorEventos
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
from src.seedwork.aplicacion.autenticacion import token_required
app = Flask(__name__)

@app.route('/')
@token_required
def home():
    return jsonify(message="Welcome to the Flask app!")

@app.route('/anonimizar-imagen', methods=['POST'])
@token_required
def anonimizar_imagen():
    try:
        if not ImagenDeAnonimizacionEsValida(request.files['image']).es_valido():
            return jsonify(error="La imagen de anonimizacion no es valida"), 400

        file = request.files['image']
        
        image_data = file.read()

        if not TamanioDeImagenEsValido(len(image_data)).es_valido():
            return jsonify(error="El tamaño de la imagen no es valido"), 400

        if not NombreDeImagenNoPuedeSerVacio(file.filename).es_valido():
            return jsonify(error="El nombre de la imagen no puede ser vacio"), 400
        
        if not FormatoDeImagenEsValido(file.filename).es_valido():
            return jsonify(error="Invalid file type, only .jpg, .png, jpeg allowed"), 400


        image_stream = BytesIO(image_data)
        image_stream2 = servicio_anonimizar_imagen(image_stream)
    
        # llamar a publicadores para publicar evento
        try:
            publicador = PublicadorEventos('pulsar://localhost:6650')
            evento = {
                'evento': 'Imagen anonimizada',
                'filename': file.filename,
                'size': len(image_data)
            }
            publicador.publicar_evento(
                'eventos-anonimizador',
                str(evento)
            )
            publicador.cerrar()
        except Exception as e:
            # Log the error but continue with the response
            print(f"Error al publicar evento: {str(e)}")
        
        return send_file(
            image_stream2,
            mimetype="image/jpeg",  # Correct MIME type for JPEG images
            as_attachment=False,    # Set to True if you want to force download
            download_name=file.filename  # Optional: Set the filename for the response
        ) 
    except Exception as e:
        return jsonify(error=f"Error inesperado: {str(e)}. Intente mas tarde.",), 500
    


