"""This module is a run script for the whole analysis procedure"""

"""
    By Kevin Kohut
"""
import os

import text_extraction
import text_analysis

script_dir = os.path.dirname(__file__)
rel_path = "../data/thesis_data.txt"
abs_file_path = os.path.join(script_dir, rel_path)
thesis_data = text_analysis.read_thesis_data(abs_file_path)

rel_path = "../data/PrototypBildMitFolie.jpeg"
abs_file_path = os.path.join(script_dir, rel_path)

text = text_extraction.extract(abs_file_path)
essential_info = text_analysis.filter_string(text[0])

print("List before scanning the document:")
text_analysis.print_still_expected_theses(thesis_data)
found_thesis = text_analysis.find_thesis(essential_info, thesis_data)

print("\nList after scanning the document:")
text_analysis.print_still_expected_theses(thesis_data)
print("\nRecognized author:", found_thesis.author.name)
print("Recognized title:", found_thesis.title)