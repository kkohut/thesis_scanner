import cv2
import numpy as np

ADAPTIVE_WINSZ = 55     # window size for adaptive threshold in reduced px


def thresh_image(image):

    # convert image from BGR to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # convert grayscale image to binary using an adaptive threshold
    image_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        ADAPTIVE_WINSZ,
                                        25)

    return image_thresh


def main():

    debug = True

    # load image
    image = cv2.imread("D:\\Coding\\thesis-scanner\\data\\1.png")

    if debug == True:
        image_thresh = thresh_image(image)
        
        cv2.imshow('Thresholded Image', image_thresh)
        cv2.waitKey()
        cv2.destroyAllWindows()
    else:
        thresh = thresh_image(image)

if __name__ == '__main__':
    main()