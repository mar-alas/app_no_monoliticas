#python3 anonimizacion_imagenes/main.py
import cv2
import easyocr
import numpy as np

def remove_text_with_easyocr(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
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

    # Save the result
    cv2.imwrite(output_path, inpainted_image)
    print(f"Text removed and image saved to {output_path}")

# Example usage
remove_text_with_easyocr("repositorio_local/imagenes_no_anonimizadas/imagen_no_anonimizada_1.jpg", "output_image.jpg")