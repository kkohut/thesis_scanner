"""This test module tests the get_date function of the date_validity.py module"""

"""
    By Melanie Willbold
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'thesis_scanner'))

import re
from datetime import datetime
from datefinder import find_dates
from langdetect import detect
from date_validity import get_date

class TestDateValidity(unittest.TestCase):
	
    def test_getDate(self):

        test_date = datetime(2020,4,20,23,59,59)
        title = "Tolles Thema über das Zeitalter Industrie 4.0"
        data = ["Hochschule für angewandte Wissenschaften", "Barbara Grünwald", "Abgabedatum:20.04.2020", "Tolles Thema über das Zeitalter Industrie 4.0"]
        self.assertEqual(detect("Attempto Controlled English für Amazon Alexa"), "en")
        self.assertEqual(detect("Analyse ausgewählter Konzepte der modernen Softwareentwicklung "), "de")
        self.assertEqual(get_date(data, title), test_date)



if __name__ == '__main__':
    unittest.main()