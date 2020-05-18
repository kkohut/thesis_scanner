"""
WORK IN PROGRESS
Input .jpeg/.png file , Output .tif file

This script is used to improve the quality of a picture before using tesseract
You put in a .png-file and get a .tif-file out with changed quality.
by Julius Bernhardt
"""
import tempfile

import cv2
import numpy as np
from PIL import Image

print("Package Imported")
path = r'C:\Users\Florentin Bernhardt\Desktop\FHWS_Progprojekt\data\T1B0.jpeg'
test = cv2.imread(path)

# 2. Resize the image
test = cv2.resize(test, None, fx=1.5, fy=1.5)
# 3. Convert image to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 4. Convert image to black and white (using adaptive threshold)
# adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

window_name = 'image'

cv2.imshow(window_name, test)
cv2.waitKey(5000)
cv2.destroyAllWindows()


def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image


set_image_dpi(path)

#remove_noise_and_smooth(test)
# cv2.imshow(window_name, img)
# cv2.waitKey(5000)
# cv2.destroyAllWindows()

cv2.imwrite('T1B1.png', test)
