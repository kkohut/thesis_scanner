"""This module contains several functions to analyze and categorize date from a string"""

from names_dataset import NameDataset

import text_extraction

import pytesseract

def get_names(text):
    """Filters and returns full names from a string

    Args:
        text: str

    Returns:
        names: list

    """
    m = NameDataset()
    words = text[0].split()
    print(words)
    names = list()
    for word in words:
        if m.search_last_name(word) == True:
            if m.search_first_name(words[words.index(word) - 1]) == True:
                first_name = words[words.index(word) - 1]
                last_name = word
                name = first_name + " " + last_name
                names.append(name)
    return names

def filter_string(text):    # not everything gets removed the right way
    filter_keywords = ["Hochschule", "angewandte", "Würzburg-Schweinfurt", "Würzburg", 
    "Schweinfurt", "Fakultät", "Bachelorarbeit", "Studiums", "Erstprüfer:", "Zweitprüfer:",
    "Eingereicht", "Dr.", "Prof."]
    filter_lines = ["", " ", "  ", "   ", "    ", "     ", ", ", " ,", ","]
    lines = text[0].split("\n")
    for line in lines:
        words = line.split()
        if line in filter_lines:
            lines.remove(line)
            continue
        for word in words:
            if word in filter_keywords:
                lines.remove(line)
                break
    filtered_text = lines
    return filtered_text

filtered_text = filter_string(text_extraction.extract("/home/kevin/MEGA/Studium/Module/SS20/Programmierprojekt/Material/Testdateien/Test_Muster/testOhneFolie01.jpg"))
names = get_names(filtered_text)