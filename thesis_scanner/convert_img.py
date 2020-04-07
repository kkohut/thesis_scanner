import sys
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

def extract_and_print(paths):
    """ extracts the text from the images given as arguments from the command line;
    returns a list of strings and prints each document
    """
    extr_strings= []
    for img in paths:
        ind = paths.index(img) + 1
        extr_string = pytesseract.image_to_string(image = Image.open(img))
        print(f"\n___________________________________________________________________\n"
            "   Document ", ind,
              "\n___________________________________________________________________")
        extr_strings.append(extr_string)
        print(extr_string)
    return extr_strings

extr_strings = extract_and_print(list(sys.argv[1:]))