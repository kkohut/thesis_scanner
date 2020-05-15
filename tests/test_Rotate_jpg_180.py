from unittest import TestCase

import cv2

from thesis_scanner.Rotate_jpg_180 import is_rotation_right, rotate_input


class Test(TestCase):

    def test_check_rotationTrue(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
        self.assertTrue(is_rotation_right(image))

    def test_check_rotationFalse(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testAufKopf02.jpg")
        self.assertFalse(is_rotation_right(image))

    def test_rotation(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testAufKopf02.jpg")
        rotatedImg = rotate_input(image)
        cv2.namedWindow("Input", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Input", image)
        cv2.imshow("Output", rotatedImg)
        cv2.waitKey()
