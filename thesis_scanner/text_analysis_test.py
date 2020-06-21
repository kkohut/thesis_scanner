"""This test module tests all the functions of the text_analysis.py module"""

"""
    By Kevin Kohut
"""

import unittest
import os
import pytesseract

import text_analysis

# DRY! -> WIP
"""def prepare_test(rel_path, script_dir, thesis_data):
    abs_file_path = os.path.join(script_dir, rel_path)
    text = pytesseract.image_to_string(abs_file_path, lang="deu").upper()

    essential_info = text_analysis.filter_string(text)
    print(essential_info)
    amount_theses_before_analysis = len(thesis_data)
    return essential_info, amount_theses_before_analysis"""


class TestThesisData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # initializes found thesis and the length of the thesis_data list before the analysis
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/thesis_data.txt"
        abs_file_path = os.path.join(script_dir, rel_path)
        cls.thesis_data = text_analysis.read_thesis_data(abs_file_path)

        #essential_info = prepare_test("../data/PrototypBildMitFolie.jpeg", script_dir, cls.thesis_data)
        #cls.found_thesis_super_mario = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation thesis 1
        rel_path = "../data/PrototypBildMitFolie.jpeg"
        abs_file_path = os.path.join(script_dir, rel_path)
        text = pytesseract.image_to_string(abs_file_path, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.amount_theses_before_analysis = len(cls.thesis_data)
        cls.found_thesis_super_mario = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 2
        rel_path = "../data/sample_max_mustermann.jpg"
        abs_file_path = os.path.join(script_dir, rel_path)
        text = pytesseract.image_to_string(abs_file_path, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_max_mustermann = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 3
        rel_path = "../data/sample_sonja_superschlau.jpg"
        abs_file_path = os.path.join(script_dir, rel_path)
        text = pytesseract.image_to_string(abs_file_path, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_sonja_superschlau = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 4
        rel_path = "../data/sample_barbara_gruenwald.jpg"
        abs_file_path = os.path.join(script_dir, rel_path)
        text = pytesseract.image_to_string(abs_file_path, lang="deu").upper()

        essential_info = text_analysis.filter_string(text)
        cls.found_thesis_barbara_gruenwald = text_analysis.find_thesis(essential_info, cls.thesis_data)

        # preparation for thesis 5
        rel_path = "../data/sample_barbara_gruenwald_2.jpg"
        abs_file_path = os.path.join(script_dir, rel_path)
        text = pytesseract.image_to_string(abs_file_path, lang="deu").upper()

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
