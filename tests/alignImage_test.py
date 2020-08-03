"""
These are the unit tests for alignImage.py.

Required packages:
    OpenCV: pip install opencv-python
    Numpy: pip install numpy
    imUtils: pip install imutils
    pytesseract: pip install pytesseract (requires Tesseract)

*** By Luca Lanzo ***
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'thesis_scanner'))
import cv2
import numpy as np
import imutils as mute
from pytesseract import image_to_string as tess
import alignImage as aI


class alignImage_test(unittest.TestCase):
    def setUp(self):
        testPicturesPath = os.path.join(os.path.dirname(__file__), "../tests/testpictures_align_image/")
        # Load images before any tests
        # for test_align_image & test_right_degree
        self.testAlignImage = cv2.imread(testPicturesPath + "testAlignImage10Degrees.jpg")
        # for test_widest_contour
        self.testPreprocessedImage = cv2.imread(testPicturesPath + "testPreprocessedImage.jpg")
        self.testWidestContour = cv2.imread(testPicturesPath + "testWidestContour.jpg")
        self.testWidestContourExpected = cv2.imread(testPicturesPath + "testWidestContourExpected.jpg")
        # for test_image_upside_down
        self.testUpsideDown = cv2.imread(testPicturesPath + "testUpsideDown.jpg")

    # Test the main function and see if the image gets aligned. Test by using Tesseract which looks for thesis and
    # author
    def test_align_image(self):
        extractedTextFromPictureNotAligned = tess(self.testAlignImage, lang="deu")

        alignedImage, _, _ = aI.align_image(self.testAlignImage)
        extractedText = tess(alignedImage, lang="deu")

        match = (("Entwicklung" in extractedText) &
                 ("eines" in extractedText) &
                 ("ganz" in extractedText) &
                 ("tollen" in extractedText) &
                 ("Algorithmus" in extractedText) &
                 ("Super" in extractedText) &
                 ("Mario" in extractedText))

        self.assertTrue(match, not (extractedTextFromPictureNotAligned))

    # Test if alignImage finds the right tilt in degrees for a picture with a know degree of tilt (10 degrees in this
    # case)
    def test_right_degree(self):
        _, _, angleInDegreesActual = aI.align_image(self.testAlignImage)
        angleInDegreesExpected = 10.0

        # Check if the found degree is inbetween a set amount of deviation
        self.assertTrue((angleInDegreesActual <= (angleInDegreesExpected + 1.0))
                        and (angleInDegreesActual >= (angleInDegreesExpected - 1.0)))

    # Test if alignImage finds the right contour on a picture. Compare the picture with the drawn contour with a
    # predrawn picture.
    def test_widest_contour(self):
        widestContour = aI.find_widest_contour(cv2.cvtColor(self.testPreprocessedImage, cv2.COLOR_BGR2GRAY))
        cv2.drawContours(self.testWidestContour, widestContour,
                         -1, (255, 200, 50), 3)

        actualImageGray = cv2.cvtColor(self.testWidestContour, cv2.COLOR_BGR2GRAY)
        expectedImageGray = cv2.cvtColor(self.testWidestContourExpected, cv2.COLOR_BGR2GRAY)

        # Difference in the actual and expected picture using the Mean Squared Error equation. The higher, the bigger
        # the difference
        difference = np.sum((actualImageGray.astype("float") - expectedImageGray.astype("float")) ** 2)
        difference /= float(actualImageGray.shape[0] * actualImageGray.shape[1])

        # Check if the difference is under a set amount of deviation
        self.assertTrue(difference <= 5.00)

    # Test if a picture on its head gets aligned the right way. Test by turning it by 180 and using Tesseract looking
    # for thesis and author
    def test_image_upside_down(self):
        extractedTextFromPictureNotAligned = tess(mute.rotate_bound(self.testUpsideDown, 180), lang="deu")

        alignedImageUpsideDown, widestContour, _ = aI.align_image(self.testUpsideDown)

        # Picture should now be aligned, but on its head, so this turns it by 180 degrees
        alignedImageUpright = mute.rotate_bound(alignedImageUpsideDown, 180)

        extractedText = tess(alignedImageUpright, lang="deu")

        match = (("Entwicklung" in extractedText) &
                 ("eines" in extractedText) &
                 ("ganz" in extractedText) &
                 ("tollen" in extractedText) &
                 ("Algorithmus" in extractedText) &
                 ("Super" in extractedText) &
                 ("Mario" in extractedText))

        self.assertTrue(match, not extractedTextFromPictureNotAligned)


if __name__ == "__main__":
    unittest.main()
