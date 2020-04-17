import cv2
import numpy as np


# load image
img = cv2.imread('D:\\Coding\\thesis-scanner\\data\\2.png')
# convert image from BGR to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# convert image to binary
ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
# get image contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# draw image contours on original image (img)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)


cv2.imshow('Needlessly Complex', img)
cv2.imwrite('2_contour.png', img)
cv2.waitKey()
cv2.destroyAllWindows()
