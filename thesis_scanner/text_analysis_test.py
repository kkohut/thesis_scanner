"""This test module tests all the functions of the text_analysis.py module"""

"""
    By Kevin Kohut
"""

import unittest
import os
import pytesseract

import text_analysis


class TestThesisData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initializes found thesis and the length of the thesis_data list before the analysis
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/thesis_data.txt"
        abs_file_path = os.path.join(script_dir, rel_path)
        cls.thesis_data = text_analysis.read_thesis_data(abs_file_path)

        rel_path = "../data/PrototypBildMitFolie.jpeg"
        abs_file_path = os.path.join(script_dir, rel_path)
        text = pytesseract.image_to_string(abs_file_path).upper()

        essential_info = text_analysis.filter_string(text)
        cls.amount_theses_before_analysis = len(cls.thesis_data)
        cls.found_thesis = text_analysis.find_thesis(essential_info, cls.thesis_data)

    def test_author(self):
        # tests if the recognized name of the author is the expected one
        self.assertEqual(self.found_thesis.author.name, "SUPER MARIO")

    def test_title(self):
        # tests if the title of the recognized thesis is as expected
        self.assertEqual(self.found_thesis.title, "ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS")

    def test_if_thesis_updated(self):
        # tests if the correct thesis entry in the list has been updated
        self.assertEqual(self.found_thesis.handed_in, True)


if __name__ == '__main__':
    unittest.main()
