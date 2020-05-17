"""This module contains several functions to analyze and categorize data from a string"""

"""Required modules:
	pytesseract: pip install pytesseract
	
    By Kevin Kohut
"""

import os
import pytesseract
#from names_dataset import NameDataset -- not used

from thesis import Author
from thesis import Thesis

def read_thesis_data(file):
    """Reads the thesis data line by line from a text file and stores it in a list

    Args:
        file: str

    Returns:

    """

    thesis_data = []
    with open(file, "r") as f:
        for line in f:
            # some names may not be unique so a counter is needed
            authors_with_this_name = 1
            # splits author and title which should be seperated by a comma
            info_splits = line.split(",")
            # removes '\n' and spaces at start and end of the string
            author_name = info_splits[0].strip()
            title = info_splits[1].strip()
            name_unique = True
            # iterates over each thesis object in the thesis_data list
            for thesis in thesis_data:
                # if the last read in author name equals the name of the author
                # of an existing thesis, increment the counter by 1
                if author_name == thesis.author.name:
                    authors_with_this_name += 1
                    name_unique = False
                    # now all authors that were read in previously have to be set to not being unique
                    for thesis in thesis_data:
                        if author_name == thesis.author.name:
                            thesis.author.name_unique = name_unique
            author = Author(name=author_name, authors_with_this_name=authors_with_this_name, name_unique=name_unique)
            thesis = Thesis(author, title)
            thesis_data.append(thesis)
    return thesis_data

def filter_string(text):
    """Filters the title and name of the author in text and returns the critical lines for further analysis

    Args:
        text: str

    Returns:
        critical_lines: list

    """

    # words that indicate a line that needs to be filtered
    filter_keywords = ["Hochschule", "angewandte", "Würzburg-Schweinfurt", "Würzburg",
                       "Schweinfurt", "Fakultät", "Bachelorarbeit", "Studiums", "Erstprüfer:", "Zweitprüfer:",
                       "Eingereicht", "Dr.", "Prof."]
    lines = text.split("\n")
    critical_lines = list()
    for line in lines:
        valid_line = True
        words = line.split()
        # remove spaces at start and end of the line
        stripped_line = line.strip()        
        # if there are only spaces and the stripped line is empty         
        # don't add it to critical_lines and continue with next line
        if len(stripped_line) == 0:
            continue                        
        for word in words:
            # if the word is in filter_keywords, don't add it to critical lines
            # and continue with next line
            if word in filter_keywords:     
                valid_line = False
                break
        # if the loop hasn't been interrupted until this point, add the line to critical_lines
        if valid_line:                      
            critical_lines.append(line)
    return critical_lines

"""
def get_names(text):    # currently not used 
    #Filters and returns full names from a string

    Args:
        text: str

    Returns:
        names: list

    m = NameDataset()
    words = text.split()
    names = list()
    for word in words:
        if m.search_last_name(word) == True:
            if m.search_first_name(words[words.index(word) - 1]) == True:
                first_name = words[words.index(word) - 1]
                last_name = word
                name = first_name + " " + last_name
                names.append(name)
    return names
    """


def compare_titles(info, theses_with_same_author_names):    # no tolerance integrated yet, just looking for the exact same title
    """

    Args:
        info: list
        theses_with_same_author_names: list

    Returns:
        thesis: Thesis
        or None

    """

    concat_lines = ""
    for line in info:
        concat_lines += " " + line
    for thesis in theses_with_same_author_names:
        # str.find(substr) equals -1 if the substring doesn't occur; if it doesn't equal 1, the title was found
        if concat_lines.find(thesis.title) != -1:
            return thesis
    return None


def find_thesis(info, thesis_data): # tolerance still needed / comparison of two titles if name is not unique
    """Looks for an author's name in each element of the info

    Args:
        info: list
        authors: list

    Returns:
        author: str

    """
                        
    # iterate over each line of the essential info
    for line in info:
        for thesis in thesis_data:
            # pos equals the position of the character of the string, where the substring starts
            pos = line.find(thesis.author.name)
            # pos equals -1 if the substring doesn't occur; if it doesn't equal 1, the name of the author was found
            if pos != -1:
                found_thesis = thesis
                if not thesis.author.name_unique:
                    current_author = thesis.author.name
                    theses_with_same_author_names = []
                    # fill the above list with all the theses entries that need to be compared
                    for thesis in thesis_data:
                        if thesis.author.name == current_author:
                            theses_with_same_author_names.append(thesis)
                    found_thesis = compare_titles(info, theses_with_same_author_names)
                    thesis_data.remove(found_thesis)
                    return found_thesis
                thesis_data.remove(thesis)
                return found_thesis
    # if none of the expected authors occurs return None    
    return None

def print_thesis(thesis):
    """Prints the data of a thesis object

    Args:
        thesis:

    Returns:

    """

    if thesis.author.name_unique:
        unique_str = "unique"
    else:
        unique_str = "not unique"
    print(f"{thesis.author.name} | {thesis.author.authors_with_this_name} | {unique_str} | {thesis.title}")

def print_still_expected_theses(thesis_data):
    """Prints the current entries of the thesis_data list

    Args:
        thesis_data: list

    Returns:

    """

    for thesis in thesis_data:
        print_thesis(thesis)