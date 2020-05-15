'''
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
from pytesseract import image_to_string


def turn_image(originalImage):
	'''
	Checks if the image is on its side and turns it by 90 degrees counterclockwise.
	This program only works with upright pictures. Upside down pictures will work too, though.
	'''
	height, width, _ = originalImage.shape

	if (height < width):
		for angle in np.arange(0, 360, 90):
			originalImage = mute.rotate(originalImage, angle)

		for angle in np.arange(0, 360, 90):
			originalImage = mute.rotate_bound(originalImage, angle)

	return originalImage


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
	unit8 -> unsigned integers ranging from 0 to 255 to save RAM
	'''
	return np.ones((h, w), dtype = np.uint8)


def dilate_image(threshedImage):
	'''
	'''
	return cv2.dilate(threshedImage, get_kernel(1, 12))


def erode_image(dilatedImage):
	'''
	'''
	return cv2.erode(dilatedImage, get_kernel(4, 1))


def find_contours(erodedImage):
	'''
	This funtion will run an algorithm on the binary picture, which will then return all the contours on the text and gets rid of false contours

	findContours function:  image = image on which cv2 is supposed to find the contours
							retrieval mode = RETR_EXTERNAL: retrieves only extreme outer contours
							approx mode = CHAIN_APPROX_NONE: stores all contour points
	boundingRect funtion: On each contour, get the corresponding rectangle with the starting x/y, as well as the height/width of the rectangle
	'''
	contours, _ = cv2.findContours(erodedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	combedContours = []

	for contour in contours:
		xbottom, ybottom, width, height = cv2.boundingRect(contour)

		# If contour is too small or too high, discard it
		if (height < 4 or width < 4 or height > 50):
			continue

		combedContours.append(contour)

	return combedContours


def find_contours_OPTIMIZED(erodedImage):
	'''
	'''
	return erodedImage


def get_PCA_orientation(contours):
	'''
	Calculates the best fitting line for a set of data points using Principal Component Analysis.
	In this context, the dataPoints equal each pixel of each contour.
	'''
	centerArray = []
	eigenvectorsArray = []
	eigenvaluesArray = []
	anglesInRadiansArray = []
	endpointsOfPCALine = []

	for c in contours:
		# put data in a nx2 matrix (i.e. matrix has only 2 columns). n is the number of data points (pixels) of each contour
		# size equals the number of pixels of the contour
		size = len(contours)
		# create an empty array -> np.empty((m = rows, n = columns))
		dataPoints = np.empty((size, 2)) # default datatype is float64 = Java "double", so pretty precise
		

		# loop through every row of the array and fill with pixels
		for i in range(dataPoints.shape[0]):
			# put x-coordinate of the pixel in the left column of the i-th row (dataPoints[row, column])
			dataPoints[i, 0] = c[i, 0, 0]
			# put y-coordinate of the pixel in the right column of the i-th row (dataPoints[row, column])
			dataPoints[i, 1] = c[i, 0, 1]


		# perform PCA analysis on set of pixels
		# mean is the center of all the scattered pixels and is where the PCA line will go through
		mean = np.empty((0)) # again with datatype float64
		mean, eigenvectors, eigenvalues = cv2.PCACompute2(dataPoints, mean)
	

		# convert the mean values from an array to a tuple (x, y)
		center = (int(mean[0, 0]), int(mean[0, 1]))
		
		
		# p1 = (center[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], center[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
		p2 = (int(center[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0]), int(center[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0]))
		
		
		# save the center, eigenvectors, eigenvalues and the angle in radians 
		centerArray.append(center)
		eigenvectorsArray.append(eigenvectors)
		eigenvaluesArray.append(eigenvalues)
		anglesInRadiansArray.append(math.atan2(eigenvectors[0,1], eigenvectors[0,0]))
		endpointsOfPCALine.append(p2)

	return centerArray, eigenvectorsArray, eigenvaluesArray, anglesInRadiansArray, endpointsOfPCALine


def get_PCA_orientation_OPTIMIZED(contours):
	'''
	'''
	return contours


def get_average_pitch(anglesInRadiansArray):
	'''
	'''
	anglesInDegreesArray = []
	sumOfRadians = 0
	
	for angle in anglesInRadiansArray:
		sumOfRadians += angle

	averagePitchInRadians = sumOfRadians / len(anglesInRadiansArray)
	averagePitchInDegrees = averagePitchInRadians * 180 / math.pi

	return averagePitchInDegrees


def get_average_pitch_OPTIMIZED(anglesInRadiansArray):
	'''
	'''
	return anglesInRadiansArray


def correct_image_rotation(originalImage, averagePitch):
	'''
	'''
	for angle in np.arange(0, 360, (averagePitch*(-1))):
		correctedImage = mute.rotate(originalImage, angle)

	#for angle in np.arange(0, 360, (averagePitch*(-1))):
	#	originalImage = mute.rotate_bound(originalImage, angle)

	return correctedImage


def main():
	debug = True

	# load image
	image = cv2.imread("D:\\Coding\\thesis-scanner\\data\\Deckblatt2.jpg")

	# check if image is on its side
	originalImage = turn_image(image)

	# threshold the image
	threshedImage = thresh_image(originalImage)

	# dilate the image
	dilatedImage = dilate_image(threshedImage)

	# erode the image
	erodedImage = erode_image(dilatedImage)

	# get image contours
	contours = find_contours(erodedImage)

	# do PCA on contours
	centerArray, eigenvectorsArray, eigenvaluesArray, anglesInRadiansArray, endpointsOfPCALine = get_PCA_orientation(contours)

	# get average pitch of the text CAREFUL, HARDCODED "IGNORE" OF THE FIRST CONTOUR BECAUSE THIS CONTOUR IS A FALSE POSITIVE
	averagePitch = get_average_pitch(anglesInRadiansArray[1:])
	print("Average pitch of the picture: ", averagePitch)

	# correct image rotation
	correctedImage = correct_image_rotation(originalImage, averagePitch)


	if debug == True:
		# Original Image
		print("\n\n\n ############# ORIGINAL IMAGE OCR: ##############\n")
		print(image_to_string(originalImage, lang = "deu"))
		
		cv2.drawContours(originalImage, contours, -1, (255, 200, 50), 1)
		
		cv2.imshow('Original Image', originalImage)
		cv2.waitKey()
		
		
		# Corrected Image
		print("\n\n\n ############# CORRECTED IMAGE OCR: ##############\n")
		print(image_to_string(correctedImage, lang = "deu"))
		
		cv2.imshow('Corrected Image', correctedImage)
		cv2.imwrite('5CorrectedImage.jpg', correctedImage)
		cv2.waitKey()

		cv2.destroyAllWindows()


if __name__ == '__main__':
	main()