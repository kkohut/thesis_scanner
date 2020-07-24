"""This test module tests the functions of the text_analysis.py module.
    It uses images without any disruptive factors such as reflections, noise or bad alignment:
    Only analysis should be tested.

    By Kevin Kohut
"""

import unittest
import os
import sys
import pytesseract

import text_analysis
import thesis_similarity
from thesis import Author
from thesis import Thesis

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'thesis_scanner'))


class TestThesisData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # initializes found thesis and the length of the thesis_data list before the analysis
        cls.rel_path = os.path.join(os.path.dirname(__file__), "testfilestextanalysis/")
                                #, "../tests/")
        cls.thesis_data = text_analysis.read_thesis_data(cls.rel_path + "thesis_data_test_1.txt")

        # preparation thesis 1
        cls.text = pytesseract.image_to_string(
            cls.rel_path + "sample_super_mario.jpg", lang="deu").upper()

        cls.essential_info = text_analysis.filter_string(cls.text)
        cls.amount_theses_before_analysis = len(cls.thesis_data)
        cls.found_thesis_super_mario = text_analysis.find_thesis(cls.essential_info, cls.thesis_data)

        # preparation for thesis 2
        cls.text = pytesseract.image_to_string(
            cls.rel_path + "sample_max_mustermann.jpg", lang="deu").upper()

        cls.essential_info = text_analysis.filter_string(cls.text)
        cls.found_thesis_max_mustermann = text_analysis.find_thesis(cls.essential_info, cls.thesis_data)

        # preparation for thesis 3
        cls.text = pytesseract.image_to_string(
            cls.rel_path + "sample_sonja_superschlau.jpg", lang="deu").upper()

        cls.essential_info = text_analysis.filter_string(cls.text)
        cls.found_thesis_sonja_superschlau = text_analysis.find_thesis(cls.essential_info, cls.thesis_data)

        # preparation for thesis 4
        cls.text = pytesseract.image_to_string(
            cls.rel_path + "sample_barbara_gruenwald.jpg", lang="deu").upper()

        cls.essential_info = text_analysis.filter_string(cls.text)
        cls.found_thesis_barbara_gruenwald = text_analysis.find_thesis(cls.essential_info, cls.thesis_data)

        # preparation for thesis 5
        cls.text = pytesseract.image_to_string(
            cls.rel_path + "sample_barbara_gruenwald_2.jpg", lang="deu").upper()

        cls.essential_info = text_analysis.filter_string(cls.text)
        cls.found_thesis_barbara_gruenwald_2 = text_analysis.find_thesis(cls.essential_info, cls.thesis_data)

    def test_correct_number_theses_in_thesis_data(self):
        # checks if number of read in theses equals 13 as expected
        self.assertEqual(len(self.thesis_data), 13)

    def test_duplicated_theses(self):
        # tests if duplicated theses are read into the list only once
        thesis_data = text_analysis.read_thesis_data(self.rel_path + "thesis_data_test_2.txt")
        # counts the amount of theses in thesis_data with an author named Super Mario
        counter = 0
        for thesis in thesis_data:
            if thesis.author.name == "SUPER MARIO":
                counter += 1
        self.assertEqual(counter, 1)

    def test_update_thesis_data(self):
        # tests if authors_with_this_name is incremented when another author with the same name is read in
        # count the amount of thesis written by authors named Barbara Grünwald
        counter = 0
        for thesis in self.thesis_data:
            if thesis.author.name == "BARBARA GRÜNWALD":
                counter += 1
        # save all values of authors_with_this_name of each thesis in a list
        authors_named_barbara_gruenwald = []
        for thesis in self.thesis_data:
            if thesis.author.name == "BARBARA GRÜNWALD":
                authors_named_barbara_gruenwald.append(thesis.author.authors_with_this_name)
        counter_equals_all_numbers = True
        # set counter_equals_all_numbers to False if an entry of the list doesn't match the counter
        for number in authors_named_barbara_gruenwald:
            if number != counter:
                counter_equals_all_numbers = False
        self.assertTrue(counter_equals_all_numbers)

    def test_filter_keywords(self):
        # tests if all keywords are filtered from essential_info
        filter_keywords = ["HOCHSCHULE", "ANGEWANDTE", "WÜRZBURG-SCHWEINFURT", "WÜRZBURG", "SCHWEINFURT", "FAKULTÄT",
                           "BACHELORARBEIT", "MASTERARBEIT", "STUDIUMS", "ERSTPRÜFER:", "ZWEITPRÜFER:", "EINGEREICHT",
                           "DR.", "PROF."]
        word_found = False
        # if one of the keywords appears in one of the filtered lines, set word_found to True
        for word in filter_keywords:
            for line in self.essential_info:
                if line.find(word) != -1:
                    word_found = True
        self.assertFalse(word_found)

    def test_swapped_names(self):
        # tests if the name can be found, if first and last names are swapped
        thesis_data = text_analysis.read_thesis_data(self.rel_path + "thesis_data_test_3.txt")
        text = pytesseract.image_to_string(self.rel_path + "sample_super_mario.jpg").upper()
        essential_info = text_analysis.filter_string(text)
        found_thesis = text_analysis.find_thesis(essential_info, thesis_data)
        # check if correct thesis could be found and the name was swapped to the correct order
        self.assertEqual(found_thesis.author.name, "SUPER MARIO")

    def test_title_similarity(self):
        # tests if similarity_1 is greater than similarity_2, it should be greater because it contains the
        # similiarity of the expected thesis title to the scanned in text
        concat_lines = " FAKULTAT INFORMATIK UND WIRTSCHAFTSINFORMATIK ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS " \
                       "WURZBURG-SCHWEINFURT IN DER FAKULTAT INFORMATIK UND WIRTSCHAFTSINFORMATIK ZUM SUPER MARIO"
        similarity_1 = thesis_similarity.cosine_similarity(thesis_similarity.string2vec(
            "ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS"),
            thesis_similarity.string2vec(concat_lines), 5)
        similarity_2 = thesis_similarity.cosine_similarity(thesis_similarity.string2vec(
            "DER BESTE ALGORITHMUS ALLER ZEITEN"), thesis_similarity.string2vec(concat_lines), 5)
        self.assertTrue(similarity_1 > similarity_2)

    def test_compare_titles(self):
        # tests if the correct thesis can be found between two theses, whose authors have the same name
        text = pytesseract.image_to_string(self.rel_path + "sample_super_mario.jpg").upper()
        essential_info = text_analysis.filter_string(text)
        # two thesis objects with authors with the same name and different thesis titles
        author_1 = Author(name="SUPER MARIO", authors_with_this_name=2, name_unique=False)
        thesis_1 = Thesis(title="DER BESTE ALGORITHMUS ALLER ZEITEN", author=author_1)
        author_2 = Author(name="SUPER MARIO", authors_with_this_name=2, name_unique=False)
        thesis_2 = Thesis(title="ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS", author=author_2)
        thesis_data = [thesis_1, thesis_2]
        thesis_with_higher_similarity = text_analysis.compare_titles(essential_info, thesis_data, thesis_1)
        self.assertEqual(thesis_with_higher_similarity.title, "ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS")

    def test_find_thesis_with_tolerance_super_murio(self):
        # tests if the correct thesis can be found with a spelling mistake in the last name
        thesis_data = text_analysis.read_thesis_data(self.rel_path + "thesis_data_test_4.txt")
        author_1 = Author(name="SUPER MURIO", authors_with_this_name=2, name_unique=False)
        thesis_1 = Thesis(title="DER BESTE ALGORITHMUS ALLER ZEITEN", author=author_1)
        thesis_data.append(thesis_1)
        text = pytesseract.image_to_string(self.rel_path + "sample_super_mario.jpg").upper()
        essential_info = text_analysis.filter_string(text)
        found_thesis = text_analysis.find_thesis_with_tolerance(essential_info, thesis_data)
        self.assertEqual(found_thesis.author.name, "SUPER MURIO")

    def test_find_thesis_with_tolerance_suber_mario(self):
        # tests if the correct thesis can be found with a spelling mistake in the first name
        thesis_data = text_analysis.read_thesis_data(self.rel_path + "thesis_data_test_4.txt")
        author_2 = Author(name="SUBER MARIO", authors_with_this_name=2, name_unique=False)
        thesis_2 = Thesis(title="ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS", author=author_2)
        thesis_data.append(thesis_2)
        text = pytesseract.image_to_string(self.rel_path + "sample_super_mario.jpg").upper()
        essential_info = text_analysis.filter_string(text)
        found_thesis = text_analysis.find_thesis_with_tolerance(essential_info, thesis_data)
        self.assertEqual(found_thesis.author.name, "SUBER MARIO")

    def test_find_thesis_with_tolerance_suber_murio(self):
        # tests if the correct thesis can be found with a spelling mistake in the first and in the last name
        thesis_data = text_analysis.read_thesis_data(self.rel_path + "thesis_data_test_4.txt")
        author_3 = Author(name="SUBER MURIO", authors_with_this_name=2, name_unique=False)
        thesis_3 = Thesis(title="ENTWICKLUNG EINES GANZ TOLLEN ALGORITHMUS", author=author_3)
        thesis_data.append(thesis_3)
        text = pytesseract.image_to_string(self.rel_path + "sample_super_mario.jpg").upper()
        essential_info = text_analysis.filter_string(text)
        found_thesis = text_analysis.find_thesis_with_tolerance(essential_info, thesis_data)
        self.assertEqual(found_thesis.author.name, "SUBER MURIO")

    def test_thesis_handed_in_is_true(self):
        self.assertTrue(self.found_thesis_super_mario.handed_in)

    def test_author_super_mario(self):
        # tests if the recognized name of the author is as expected
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
