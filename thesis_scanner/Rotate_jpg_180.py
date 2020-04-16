import cv2
import pytesseract as tess
from PIL import Image


def rotate_input(image: Image):
    rotatedImg = cv2.flip(image, -1)
    return rotatedImg

# flipcode = 0: flip vertically
#  flipcode > 0: flip horizontally
#  flipcode < 0: flip vertically and horizontally


def is_rotation_right(image: Image):
    text = tess.image_to_string(image, "deu")
    if "Erstpruefer" in text or "Erstprüfer" in text:
        # print("true")
        return True
    else:
        # print("false")
        return False
