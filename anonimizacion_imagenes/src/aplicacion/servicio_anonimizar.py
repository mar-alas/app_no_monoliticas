#python3 anonimizacion_imagenes/main.py
from io import BytesIO
import cv2
import easyocr
import numpy as np
from src.infraestructura.publicadores import PublicadorEventos
from src.seedwork.infraestructura.utils import broker_host
from src.seedwork.dominio.reglas import FormatoDeImagenEsValido, NombreDeImagenNoPuedeSerVacio, ImagenDeAnonimizacionEsValida, TamanioDeImagenEsValido
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def servicio_anonimizar_imagen(image_name:str,binary_image:BytesIO)->BytesIO:
    try:
        if not ImagenDeAnonimizacionEsValida(binary_image).es_valido():
            raise ValueError("Imagén de anonimización no válida")
        
        if not TamanioDeImagenEsValido(len(binary_image.getbuffer())).es_valido():
            raise ValueError("El tamaño de la imagen no es válido")

        if not NombreDeImagenNoPuedeSerVacio(image_name).es_valido():
            raise ValueError("El nombre de la imagen no puede ser vacio")

        if not FormatoDeImagenEsValido(image_name).es_valido():
            raise ValueError("El formato de la imagen no es valido")
        
        # Load the image
        image = cv2.imdecode(np.frombuffer(binary_image.getbuffer(), np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Image not found or unable to load.")

        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Detect text regions
        results = reader.readtext(image)

        # Create a mask for inpainting
        mask = np.zeros_like(image[:, :, 0])

        # Loop over detected text regions
        for (bbox, text, prob) in results:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            # Draw a white rectangle on the mask where text is detected
            cv2.rectangle(mask, top_left, bottom_right, (255), -1)

        # Use inpainting to remove the text
        inpainted_image = cv2.inpaint(image, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

        # save result to binary
        _, buffer = cv2.imencode('.jpeg', inpainted_image)
        binary_image_data = BytesIO(buffer)

        pulsar_host=broker_host()
        publicador = PublicadorEventos(f'pulsar://{pulsar_host}:6650')
        evento = {
            'evento': 'Imagen anonimizada',
            'filename': image_name,
            'size': binary_image_data.getbuffer().nbytes
        }
        publicador.publicar_evento(
            'eventos-anonimizador',
            str(evento)
        )
        publicador.cerrar()

        return binary_image_data
    
    except Exception as e:
        logger.error(f"Error procesando comando de ingesta: {str(e)}")
