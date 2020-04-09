"""This script allows to call the extract_and_print function from the thesis_scanner.text_extraction module
usable by appending one or more image file paths to the command
callable with this command: python3 -m scripts/print_texts file_path_1 file_path_2 file_path_n
"""

import sys

from thesis_scanner import text_extraction

extr_strings = text_extraction.extract_and_print(list(sys.argv[1:]))