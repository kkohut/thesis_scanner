import os
import cv2
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'thesis_scanner'))
import alignImage as aI


class alignImage_test(unittest.TestCase):
    def setUp(self):
        # The setup before any test
        # Load image, preprocess it and return the widest contour and angle
        # so that it can be worked on in each individual test

        absImagePath = os.path.join(os.path.dirname(__file__), "../data/testOhneFolie10.jpg")

        self.image = cv2.imread(absImagePath)
        self.preProcessedImage = aI.erode_image(aI.dilate_image(aI.thresh_image(aI.turn_image(self.image))))
        self.widestContour = aI.find_widest_contour(self.preProcessedImage)
        _, _, _, angleInRadians = aI.do_PCA(self.widestContour)
        self.angleInDegrees = aI.get_angle_in_degrees(angleInRadians)

    def test_checkIfAngleIsRight(self):
        # This first test checks if 
        self.assertEqual(int(self.angleInDegrees), int(6.549000525100995))

        
if __name__ == "__main__":
    unittest.main()