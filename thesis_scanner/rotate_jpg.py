'''
Required packages:
    OpenCV: pip install opencv-python
    Numpy: pip install numpy
    imUtils: pip install imutils
'''

import cv2
import numpy as np
import imutils as mute

def turn_image(image):
    '''
    Checks if the image is on its side and turns it by 90 degrees counterclockwise.
    This program only works with upright pictures. Upside down pictures will work too, though.
    '''
    height, width, _ = image.shape

    if (height < width):
        for angle in np.arange(0, 360, 90):
	        image = mute.rotate(image, angle)

        for angle in np.arange(0, 360, 90):
	        image = mute.rotate_bound(image, angle)

    return image


def thresh_image(image_turned):
    '''
    Converts image from BGR to grayscale
    Then converts grayscale image to binary using an adaptive threshold
    '''
    image_gray = cv2.cvtColor(image_turned, cv2.COLOR_BGR2GRAY)
    image_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 55, 25)

    return image_thresh


def get_kernel(h, w):
    '''
    unit8 -> unsigned integers ranging from 0 to 255
    '''
    return np.ones((h, w), dtype = np.uint8)


def dilate_image(image_thresh):
    '''
    '''
    return cv2.dilate(image_thresh, get_kernel(1, 12))



def erode_image(image_dilate):
    '''
    '''
    return cv2.erode(image_dilate, get_kernel(4, 1))


def find_contours(image_erode):
    '''
    This funtion will run an algorithm on the binary picture, which will then return all the contours on the text and gets rid of false contours

    findContours function:  image = image on which cv2 is supposed to find the contours
                            retrieval mode = RETR_EXTERNAL: retrieves only extreme outer contours 
                            approx mode = CHAIN_APPROX_NONE: stores all contour points
    boundingRect funtion: On each contour, get the corresponding rectangle with the starting x/y, as well as the height/width of the rectangle
    '''

    contours, _ = cv2.findContours(image_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    combed_contours = []

    for contour in contours:
        xbottom, ybottom, width, height = cv2.boundingRect(contour)

        # If contour is too small or too high, discard it
        if (height < 4 or width < 4 or height > 50):
            continue

        combed_contours.append(contour)

    return combed_contours


def main():
    debug = True

    # load image
    image = cv2.imread("D:\\Coding\\thesis-scanner\\data\\Deckblatt5.jpg")
    # check if image is on its side
    image = turn_image(image)
    # threshold the image
    image_thresh = thresh_image(image)
    # dilate the image
    image_dilate = dilate_image(image_thresh)
    # erode the image
    image_erode = erode_image(image_dilate)
    # get image contours
    image_contours = find_contours(image_erode)

    if debug == True:
        cv2.drawContours(image, image_contours, -1, (0, 0, 255), 2)
        
        cv2.imshow('Imageview', image)
        cv2.waitKey()
        cv2.destroyAllWindows()
 

if __name__ == '__main__':
    main()