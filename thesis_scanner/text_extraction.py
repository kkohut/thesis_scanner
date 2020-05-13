"""This module contains several functions to handle text extraction and printing from image files"""

"""Required modules:
	pytesseract: pip install pytesseract
	PIL: pip install pillow
	
    By Kevin Kohut
"""

import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

def print_text_strings(strings):
    """Prints the list of strings given as an argument

    Args:
        strings: list

    Returns:

    """
    for s in strings:
        ind = strings.index(s) + 1
        if len(strings) > 1:
            print(f"\n___________________________________________________________________\n"
                "   Text", ind,
                "\n___________________________________________________________________\n")
        print(s)

def extract(paths):
    """Extracts the text from the images given and returns them as a list of strings
    argument can be a string or a list of strings

    Args:
        paths: str or list

    Returns:
        extr_strings: list

    """
    if type(paths) == str:
        paths = [paths]
    extr_strings = []
    for img in paths:
        extr_string = pytesseract.image_to_string(image=Image.open(img), lang="deu")
        extr_strings.append(extr_string)
    return extr_strings

def extract_and_print(paths):
    """Extracts and prints the text from the images given as argument from the command line
    returns a list of strings and prints each document

    Args:
        paths: str or list

    Returns:
        extr_strings: list

    """
    extr_strings = extract(paths)
    print_text_strings(extr_strings)
    return extr_strings