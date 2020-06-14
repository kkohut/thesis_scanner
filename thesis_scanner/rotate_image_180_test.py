from unittest import TestCase

import cv2

from thesis_scanner.rotate_image_180 import check_rotation, rotate_input


class Test(TestCase):

    # tests to check if the function returns True if image has right rotation
    # "standard image"
    def test_check_rotationTrue_ohne_folie(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    # image from thesis in prototype box
    def test_check_rotationTrue_protoytp(self):
        image = cv2.imread(r"../data/PrototypBildMitFolie.jpeg")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    # thesis with a special font
    def test_check_rotationTrue_special_font(self):
        image = cv2.imread(r"../data/donald_duck.png")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    # thesis with bold letters
    def test_check_rotationTrue_bold_font(self):
        image = cv2.imread(r"../data/lothar_lastminute.png")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    # thesis on green paper
    def test_check_rotationTrue_green_paper(self):
        image = cv2.imread(r"../data/green.png")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    # thesis on black paper with white letters
    def test_check_rotationTrue_black_paper(self):
        image = cv2.imread(r"../data/black.png")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)

    # thesis on blue paper with black letters
    def test_check_rotationTrue_blue_paper(self):
        image = cv2.imread(r"../data/blue.png")
        rotation, text = check_rotation(image)
        self.assertTrue(rotation)


    # tests to check if the function returns False if image has wrong rotation
    def test_check_rotationFalse(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testAufKopf02.jpg")
        rotation, text = check_rotation(image)
        self.assertFalse(rotation)

    def test_check_rotationFalse_2(self):
        image = cv2.imread(r"../data/donald_duck_auf_kopf.png")
        rotation, text = check_rotation(image)
        self.assertFalse(rotation)

    def test_check_rotationFalse_3(self):
        image = cv2.imread(r"../data/peter_panik_auf_kopf.png")
        rotation, text = check_rotation(image)
        self.assertFalse(rotation)

    # test the rotation and shows input and output on the screen
    def test_check_rotation(self):
        image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testAufKopf02.jpg")

        image_rotated, text = rotate_input(image)
        cv2.namedWindow("Input", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Input", image)
        cv2.imshow("Output", image_rotated)
        cv2.waitKey(2000)
