'''
This Python program takes an image that is slightly turned, calculate the pitch and turn it upright.

Required packages:
	OpenCV: pip install opencv-python
	Numpy: pip install numpy
	imUtils: pip install imutils
	math: Only import from Python standard library

*** By Luca Lanzo ***
'''

import cv2
import numpy as np
import imutils as mute
import math


def turn_image(image):
	'''
	Checks if the image is on its side and turns it by 90 degrees counterclockwise.
	'''
	height, width, _ = image.shape

	if (height < width):
		return mute.rotate_bound(image, 90)
	else:
		return image


def thresh_image(turnedImage):
	'''
	Converts image from BGR to grayscale
	Then converts grayscale image to binary using an adaptive threshold
	'''
	grayedImage = cv2.cvtColor(turnedImage, cv2.COLOR_BGR2GRAY)
	threshedImage = cv2.adaptiveThreshold(grayedImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 55, 25)

	return threshedImage


def get_kernel(h, w):
	'''
	This method is critical for the dilation and erosion methods. This kernel represents a box that can be shaped by height and width and will later on
	determine in which direction and how far the dilation and erosion should go.
	It returns and array with an interchangeable size which serves as a blueprint.
	'''
	return np.ones((h, w), dtype = np.uint8)


def dilate_image(threshedImage):
	'''
	This method dilates the white pixels in the image to make them "bigger" to the left and right. 
	This ensures that the following contour detection won't only detect single letters but rather full lines of text.
	'''
	return cv2.dilate(threshedImage, get_kernel(1, 12))


def erode_image(dilatedImage):
	'''
	This method erodes the lines of text to the top and bottom.
	This ensures that minor pixel deviations to the top or bottom are evened out so multiple lines of text don't connect to each other and form big text blobs.
	'''
	return cv2.erode(dilatedImage, get_kernel(4, 1))


def find_widest_contour(erodedImage):
	'''
	This function will run an algorithm on the binary picture which will then find all the contours on each pixel blob.
	To save space, time and optimize the pitch analysis, only the widest contour will be returned (and the second widest for an error fallback).

	findContours function:  image = image on which cv2 is supposed to find the contours
							retrieval mode = RETR_EXTERNAL: retrieves only extreme outer contours
							approx mode = CHAIN_APPROX_NONE: stores all contour points
	boundingRect funtion: On each contour, get the corresponding rectangle with the starting x/y, as well as the width, height of the rectangle
	'''
	contours, _ = cv2.findContours(erodedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	widestContour = contours[0]
	
	# find widest contour
	for contour in contours:
		_, _, newContourWidth, _ = cv2.boundingRect(contour)
		_, _, oldcontourWidth, _ = cv2.boundingRect(widestContour)
		
		if newContourWidth >= oldcontourWidth:
			widestContour = contour
		else:
			continue

	return widestContour


def do_PCA(widestContour):
	'''
	Calculates the best fitting line for a set of data points using Principal Component Analysis.
	In this context, the set of dataPoints equals the set of pixels of the widest contour.
	The pixels can be interpreted as coordinates in a coordinate system and PCA will find a line that is essentially the median of all points.
	PCA is perfect for reducing dimensionalities. Our sets of pixel are scattering over a coordinate system in a two dimensional manner, while
	the PCA line is one dimensional. This reduces the complexity of the program and improves the runtime.
	'''
	
	dataPoints = np.empty((len(widestContour), 2), dtype = np.float64)

	for i, dp in enumerate(dataPoints):
		# put the x coordinate of the pixel[i] in the left column of the dataset
		dp[0] = widestContour[i, 0, 0]
		# put the y coordinate of the pixel[i] in the right column of the dataset
		dp[1] = widestContour[i, 0, 1]
	

	mean = np.empty((0), dtype = np.float64)
	mean, eigenvectors, eigenvalues = cv2.PCACompute2(dataPoints, mean)

	center = (int(mean[0, 0]), int(mean[0, 1]))
	angleInRadians = math.atan2(eigenvectors[0, 1], eigenvectors[0, 0])

	return center, eigenvectors, eigenvalues, angleInRadians


def get_angle_in_degrees(angleInRadians):
	'''
	Converts the angle of the text from radians to degrees.
	'''
	return angleInRadians * 180 / math.pi


def correct_image_alignment(image, angleInDegrees):
	'''
	Corrects the image pitch using the inverse of the calculated angle in degrees 
	'''
	return mute.rotate_bound(image, angleInDegrees * (-1))


def align_image(image):
	# turn, thresh, dilate and erode the original image using the preprocessing methods
	preprocessedImage = erode_image(dilate_image(thresh_image(turn_image(image))))

	# find the widest contour
	widestContour = find_widest_contour(preprocessedImage)

	# find a best fit line for the widest contour using PCA
	center, eigenvectors, eigenvalues, angleInRadians = do_PCA(widestContour)

	# convert the angle of the best fit line from radians to degrees
	angleInDegrees = get_angle_in_degrees(angleInRadians)

	# reverse the image rotation using the calculated pitch
	return correct_image_alignment(image, angleInDegrees)
