import cv2
import numpy as np


def thresh_image(image):
    '''
    Converts image from BGR to grayscale
    Then converts grayscale image to binary using an adaptive threshold
    '''
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 55, 25)

    return image_thresh


def get_kernel(w, h):
    '''
    unit8 -> unsigned integers ranging from 0 to 255
    '''
    return np.ones((h, w), dtype = np.uint8)


def dilate_image(image_thresh):
    '''
    '''
    return cv2.dilate(image_thresh, get_kernel(9, 1))



def erode_image(image_dilate):
    '''
    '''
    return cv2.erode(image_dilate, get_kernel(1, 3))


def find_contours(image_erode):
    '''
    '''
    contours, _ = cv2.findContours(image_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

    combed_contours = np.array()

    for contour in contours:
        xbottom, ybottom, width, height = cv2.boundingRect(contour)

        if (width < 15):
            continue


def main():
    debug = True

    # load image
    image = cv2.imread("D:\\Coding\\thesis-scanner\\data\\1.png")
    # threshold the image
    image_thresh = thresh_image(image)
    # dilate the image
    image_dilate = dilate_image(image_thresh)
    # erode the image
    image_erode = erode_image(image_dilate)
    # get image contours
    image_contours = find_contours(image_erode)

    if debug == True:
        cv2.drawContours(image, image_contours, -1, (255, 0, 0), 1)
        
        cv2.imshow('Imageview', image)
        cv2.waitKey()
        cv2.destroyAllWindows()
 

if __name__ == '__main__':
    main()