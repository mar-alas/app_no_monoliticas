#python3 anonimizacion_imagenes/main.py
from io import BytesIO
import cv2
import easyocr
import numpy as np

def servicio_anonimizar_imagen(binary_image:BytesIO)->BytesIO:
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
    return binary_image_data

