"""This test module tests all the functions of the text_analysis.py module"""

import unittest
import os

import text_extraction
import text_analysis

class TestThesisData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initializes author, title and the length of the thesis_data dictionary before the analysis
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/thesis_data.txt"
        abs_file_path = os.path.join(script_dir, rel_path)
        cls.thesis_data = text_analysis.read_thesis_data(abs_file_path)

        rel_path = "../data/PrototypBildMitFolie.jpeg"
        abs_file_path = os.path.join(script_dir, rel_path)
        texts = text_extraction.extract(abs_file_path)
        
        essential_info = text_analysis.filter_string(texts[0])
        cls.amount_thesis_before_analysis = len(cls.thesis_data)
        cls.author, cls.title = text_analysis.find_author_and_title(essential_info, cls.thesis_data)

    def test_author(self):
        # tests if the recognized name of the author is the expected one
        self.assertEqual(self.author, "Super Mario")
    
    def test_title(self):
        # tests if the title of the thesis is as expected
        self.assertEqual(self.title, "Entwicklung eines ganz tollen Algorithmus")

    def test_if_key_removed(self):
        # tests if the author has been removed from the dictionary after the recognition of the data and if the size of the dictionary decremented by 1
        self.assertNotIn(self.author, self.thesis_data)
        self.assertEqual(len(self.thesis_data), self.amount_thesis_before_analysis - 1)

if __name__ == '__main__':
    unittest.main()