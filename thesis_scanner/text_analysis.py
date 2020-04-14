"""This module contains several functions to analyze and categorize date from a string"""

from names_dataset import NameDataset

from thesis_scanner import text_extraction

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