"""
Input .jpeg/.png file , Output .tif file

This script is used to improve the quality of a picture before using tesseract
by Julius Bernhardt
"""
import tempfile
import tempfile

import cv2
import os
import numpy as np
from PIL import Image


#get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)


#thresholding
def thresholding(image):
   return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 55, 25)


#blur
def blur(image):
    return cv2.GaussianBlur(image,(5,5),0)


#defilation
def dilate(image):
    kernel = np.ones((7,7),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)


#erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)



#runscript
def picture_quality_improve(image):
    image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    image = get_grayscale(image)
    image = blur(image)
    image = remove_noise(image)
    image = thresholding(image)
    image = dilate(image)
    image = erode(image)
    image = opening(image)
    return image


