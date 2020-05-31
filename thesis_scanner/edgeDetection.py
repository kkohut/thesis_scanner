'''
This Python program takes an image and deletes unnecessary noise around a white DIN A4 page. It calculates the edges of the page and
cuts the noise out accordingly.
	
Required packages:
	OpenCV: pip install opencv-python
	Numpy: pip install numpy

*** By Luca Lanzo ***
'''

import cv2
import numpy as np


def find_edge(image):
	image = cv2.Canny(image, 100, 300, 3)
	contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	biggestContour = contours[0]
	for contour in contours:
		if (cv2.arcLength(contour, False) > cv2.arcLength(biggestContour, False)):
			biggestContour = contour

	return biggestContour


def apply_convex_hull_algorithm(biggestContour):
	return cv2.convexHull(biggestContour)


def cut_image(image, biggestContour):
	x, y, width, height = cv2.boundingRect(biggestContour)
	image = image[y:height, x:width].copy()

	return image


def detect_edges(originalImage):
	# Find the contour with the biggest edge length, which equals the edge of the document
	biggestContour = find_edge(originalImage)

	# Apply Convex hull algorithm to bridge the deflection in the straight lines
	biggestContourHull = cv2.convexHull(biggestContour)

	# Cut the picture around the edge of the document
	cutImage = cut_image(originalImage, biggestContour)

	return cutImage
