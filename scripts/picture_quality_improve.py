"""
WORK IN PROGRESS
Input .jpeg/.png file , Output .tif file

This script is used to improve the quality of a picture before using tesseract
You put in a .png-file and get a .tif-file out with changed quality.
by Julius Bernhardt
"""

import cv2
print("Package Imported")

img = cv2.imread('T1B0.jpeg', -1)


# 2. Resize the image
#img = cv2.resize(img, None, fx=0.5, fy=0.5)
# 3. Convert image to grayscale
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 4. Convert image to black and white (using adaptive threshold)
#adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)


cv2.imshow('Display window', img)
cv2.waitKey(5000)
cv2.destroyAllWindows()

cv2.imwrite('T1B1.tif', img);