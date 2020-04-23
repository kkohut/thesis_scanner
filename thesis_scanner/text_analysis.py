"""This module contains several functions to analyze and categorize data from a string"""

from names_dataset import NameDataset

import text_extraction

import pytesseract

def filter_string(text):
    """Filters the title and name of the author in text and returns the critical lines for further analysis

    Args:
        text: str

    Returns:
        critical_lines: list

    """
    filter_keywords = ["Hochschule", "angewandte", "Würzburg-Schweinfurt", "Würzburg", 
    "Schweinfurt", "Fakultät", "Bachelorarbeit", "Studiums", "Erstprüfer:", "Zweitprüfer:",
    "Eingereicht", "Dr.", "Prof."]          # words that indicate a line that needs to be filtered
    lines = text[0].split("\n")
    critical_lines = list()
    for line in lines:
        valid_line = True
        words = line.split()
        stripped_line = line.strip()        # remove spaces at start and end of the line
        if len(stripped_line) == 0:         # if there are only spaces and the stripped line is empty
            continue                        # don't add it to critical_lines and continue with next line
        for word in words:
            if word in filter_keywords:     # if the word is in filter_keywords, don't add it to critical lines
                valid_line = False          # and continue with next line
                break
        if valid_line:                      # if the loop hasn't been interrupted until this point, add the line to critical_lines
            critical_lines.append(line)
    return critical_lines

def get_names(text):
    """Filters and returns full names from a string

    Args:
        text: str

    Returns:
        names: list

    """
    m = NameDataset()
    words = text[0].split()
    names = list()
    for word in words:
        if m.search_last_name(word) == True:
            if m.search_first_name(words[words.index(word) - 1]) == True:
                first_name = words[words.index(word) - 1]
                last_name = word
                name = first_name + " " + last_name
                names.append(name)
    return names