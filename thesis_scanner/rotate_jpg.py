'''
Required packages:
	OpenCV: pip install opencv-python
	Numpy: pip install numpy
	imUtils: pip install imutils
'''

import cv2
import numpy as np
import imutils as mute

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
	unit8 -> unsigned integers ranging from 0 to 255
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


def find_contours(image_erode):
	'''
	This funtion will run an algorithm on the binary picture, which will then return all the contours on the text and gets rid of false contours

	findContours function:  image = image on which cv2 is supposed to find the contours
							retrieval mode = RETR_EXTERNAL: retrieves only extreme outer contours
							approx mode = CHAIN_APPROX_NONE: stores all contour points
	boundingRect funtion: On each contour, get the corresponding rectangle with the starting x/y, as well as the height/width of the rectangle
	'''
	contours, _ = cv2.findContours(image_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	combedContours = []

	for contour in contours:
		xbottom, ybottom, width, height = cv2.boundingRect(contour)

		# If contour is too small or too high, discard it
		if (height < 4 or width < 4 or height > 50):
			continue

		combedContours.append(contour)

	return combedContours


def get_PCA_orientation(contours):
	'''

	'''
	meanArray, eigenvectorsArray, eigenvaluesArray = []

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

		# save the center of the object
		centerPCALine = (int(mean[0, 0]), int(mean[0, 1]))
		
		meanArray.append(mean)
		eigenvectorsArray.append(eigenvectors)
		eigenvaluesArray.append(eigenvalues)

	return meanArray, eigenvectorsArray, eigenvaluesArray()


def main():
	debug = True

	# load image
	originalImage = cv2.imread("D:\\Coding\\thesis-scanner\\data\\Deckblatt2.jpg")

	# check if image is on its side
	originalImage = turn_image(originalImage)

	# threshold the image
	threshedImage = thresh_image(originalImage)

	# dilate the image
	dilatedImage = dilate_image(threshedImage)

	# erode the image
	erodedImage = erode_image(dilatedImage)

	# get image contours
	contours = find_contours(erodedImage)

	if debug == True:
		cv2.drawContours(originalImage, contours, 8, (255, 200, 50), 2)

		# height, width, _ = originalImage.shape
		# cv2.line (..., (smaller x, and y), (bigger x, and y), ...)
		# cv2.line(originalImage, (10, 0 + 10), (width - 10, height - 10), (255, 200, 50), 2)
		# cv2.line(originalImage, (width-10, int(height/2)), (10, int(height/2)), (255, 200, 50), 2)
		
		cv2.imshow('Imageview', originalImage)
		cv2.waitKey()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	main()