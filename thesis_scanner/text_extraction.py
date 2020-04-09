"""This module contatains several functions to handle text extraction and printing from image files"""

import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

def print_text_strings(strings):
    """prints the list of strings given as an argument"""
    for s in strings:
        ind = strings.index(s) + 1
        if len(strings) > 1:
            print(f"\n___________________________________________________________________\n"
                "   Text", ind,
                "\n___________________________________________________________________\n")
        print(s)

def extract(paths):
    """extracts the text from the images given and returns them as a list of strings"""
    extr_strings = []
    for img in paths:
        extr_string = pytesseract.image_to_string(image=Image.open(img), lang="deu")
        extr_strings.append(extr_string)
    return extr_strings

def extract_and_print(paths):
    """extracts the text from the images given as argument from the command line
    returns a list of strings and prints each document
    """
    extr_strings = extract(paths)
    print_text_strings(extr_strings)
    return extr_strings