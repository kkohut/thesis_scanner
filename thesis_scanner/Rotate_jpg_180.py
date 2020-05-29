import cv2
import pytesseract as tess
from PIL import Image


def rotate_input(image: Image):
    ''' Checks if the image is upside down and rotate it if required

    :param image: Image
    :return:(rotated)image: Image

    '''
    if is_rotation_right(image):
        return image
    else:
        rotated_image = cv2.flip(image, -1)
        #flipcode < 0: flip vertically and horizontally
        return rotated_image


def is_rotation_right(image: Image):
    """ Checks if the image is upside down,
        if the image is in right direction the function returns True
        if the image is upside down the function returns False

    :param image: Image
    :return:boolean
    """
    text = (tess.image_to_string(image, "deu")).upper()
    if "BACHELOR" in text or "MASTER" in text or "THESIS" in text or "ARBEIT" in text:
        return True
    else:
        return False
