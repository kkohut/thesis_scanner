"""This test module tests the functions of the text_analysis.py module"""

"""
    By Kevin Kohut
"""

import unittest
import os
import sys
import pytesseract

import text_analysis

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'thesis_scanner'))


class TestThesisData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # initializes found thesis and the length of the thesis_data list before the analysis
        rel_path = os.path.join(os.path.dirname(__file__), "../tests/")
        cls.thesis_data = text_analysis.read_thesis_data(rel_path + "../data/thesis_data.txt")

        # preparation thesis 1
        path_to_picture = "testpicturestextanalysis/sample_super_mario.jpg"
        text = pytesseract.image_to_string(rel_path + path_to_picture, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.amount_theses_before_analysis = len(cls.thesis_data)
        cls.found_thesis_super_mario = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 2
        path_to_picture = "testpicturestextanalysis/sample_max_mustermann.jpg"
        text = pytesseract.image_to_string(rel_path + path_to_picture, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_max_mustermann = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 3
        path_to_picture = "testpicturestextanalysis/sample_sonja_superschlau.jpg"
        text = pytesseract.image_to_string(rel_path + path_to_picture, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_sonja_superschlau = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 4
        path_to_picture = "testpicturestextanalysis/sample_barbara_gruenwald.jpg"
        text = pytesseract.image_to_string(rel_path + path_to_picture, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_barbara_gruenwald = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 5
        path_to_picture = "testpicturestextanalysis/sample_barbara_gruenwald_2.jpg"
        text = pytesseract.image_to_string(rel_path + path_to_picture, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_barbara_gruenwald_2 = text_analysis.find_thesis(essential_info, cls.thesis_data)

    def test_author_super_mario(self):
        # tests if the recognized name of the author is the expected one
        self.assertEqual(self.found_thesis_super_mario.author.name, "SUPER MARIO")

    def test_title_super_mario(self):
        # tests if the title of the recognized thesis is as expected
        self.assertEqual(self.found_thesis_super_mario.title, "ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS")

    def test_if_thesis_updated(self):
        # tests if the correct thesis entry in the list has been updated
        self.assertEqual(self.found_thesis_super_mario.handed_in, True)

    def test_author_max_mustermann(self):
        self.assertEqual(self.found_thesis_max_mustermann.author.name, "MAX MUSTERMANN")

    def test_title_max_mustermann(self):
        self.assertEqual(self.found_thesis_max_mustermann.title, "FLUSSERKENNUNG AUF LUFTAUFNAHMEN DURCH MASCHINELLES "
                                                                 "LERNEN")

    def test_author_sonja_superschlau(self):
        self.assertEqual(self.found_thesis_sonja_superschlau.author.name, "SONJA SUPERSCHLAU")

    def test_title_sonja_superschlau(self):
        self.assertEqual(self.found_thesis_sonja_superschlau.title, "VERBRAUCHER-TRACKING IN DER DATENÖKONOMIE UND "
                                                                    "ALGORITHMISCHE ENTSCHEIDUNGSFINDUNG")

    def test_author_barbara_gruenwald(self):
        self.assertEqual(self.found_thesis_barbara_gruenwald.author.name, "BARBARA GRÜNWALD")

    def test_title_barbara_gruenwald(self):
        self.assertEqual(self.found_thesis_barbara_gruenwald.title, "ANWENDUNGSMÖGLICHKEITEN UND RISIKEN DER BLOCKCHAIN"
                                                                    " IM WEB 3.0")

    def test_author_barbara_gruenwald_2(self):
        self.assertEqual(self.found_thesis_barbara_gruenwald_2.author.name, "BARBARA GRÜNWALD")

    def test_title_barbara_gruenwald_2(self):
        self.assertEqual(self.found_thesis_barbara_gruenwald_2.title, "EINSATZ UND FUNKTION DER POLYGONE IN DER "
                                                                      "3D-MODELLIERUNG")


if __name__ == '__main__':
    unittest.main()
