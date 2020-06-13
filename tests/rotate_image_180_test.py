from unittest import TestCase

import cv2

from thesis_scanner.rotate_image_180 import check_rotation, rotate_input


class Test(TestCase):

    def test_check_rotationTrue(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    def test_check_rotationFalse(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testAufKopf02.jpg")
        rotation, text = check_rotation(image)
        self.assertFalse(rotation)

    def test_rotation(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testAufKopf02.jpg")

        image_rotated, text = rotate_input(image)
        cv2.namedWindow("Input", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Input", image)
        cv2.imshow("Output", image_rotated)
        cv2.waitKey()
