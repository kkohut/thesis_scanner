import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'thesis_scanner'))

import cv2
import numpy as np
from pytesseract import image_to_string as read
from thesis_scanner import picture_quality_improve as pqi

#Testcase

class alignImage_test1(unittest.TestCase):
    def setUp(self):
        testPicturesPath = os.path.join(os.path.dirname(__file__), "../tests/testpictures_quality_improve/")
        # Load images before any tests

        # The picture we use has a bad quality, the author can not be found without using picture_quality_improve
        self.testqualityPic = cv2.imread(testPicturesPath + "Test_Donald.jpg")
    #Test: The author will not be found in this unimproved picture
    def test_quality_unimproved(self):
        quality_unimproved = self.testqualityPic
        text = read(quality_unimproved, lang="deu")

        match = ("Donald" in text)
        self.assertFalse(match)
    #Test: Testing the function of the improvement. After using picture_quality_improve the author will be found
    def test_quality_improved(self):
        quality_improved = pqi.picture_quality_improve(self.testqualityPic)
        text = read(quality_improved, lang="deu")

        match = ("Donald" in text)
        self.assertTrue(match)




if __name__ == '__main__':
    unittest.main()
