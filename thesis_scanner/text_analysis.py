"""This module contains several functions for extracting, analyzing and categorizing data from a string"""

"""Required modules:
    PIL: pip install pillow
	pytesseract: pip install pytesseract
	textdistance: pip install textdistance
	
    By Kevin Kohut
"""

import textdistance

try:
    from PIL import Image
except ImportError:
    import Image

from thesis import Author
from thesis import Thesis


def read_thesis_data(file):
    """Reads the thesis data line by line from a text file and stores it in a list

    Args:
        file: str

    Returns:
        thesis_data: list

    """

    thesis_data = []
    with open(file, "r") as f:
        for line in f:
            line = line.upper()
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
    filter_keywords = ["HOCHSCHULE", "ANGEWANDTE", "WÜRZBURG-SCHWEINFURT", "WÜRZBURG", "SCHWEINFURT", "FAKULTÄT",
                       "BACHELORARBEIT", "MASTERARBEIT", "STUDIUMS", "ERSTPRÜFER:", "ZWEITPRÜFER:", "EINGEREICHT",
                       "DR.", "PROF."]
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


def compare_titles(info, theses_with_same_author_names):  # no tolerance integrated yet, just looking for the exact same title
    """

    Args:
        info: list
        theses_with_same_author_names: list

    Returns:
        thesis: Thesis

    """

    concat_lines = ""
    title_similarity = {}
    highest_similarity = 0
    # create one concatenated string consisting of all remaining lines
    for line in info:
        concat_lines += " " + line
    for thesis in theses_with_same_author_names:
        # get similarity between the title of the currently compared thesis and the string
        similarity = textdistance.ratcliff_obershelp(concat_lines, thesis.title)
        # find the highest similarity
        if similarity >= highest_similarity:
            highest_similarity = similarity
            thesis_with_highest_similarity = thesis
        # add thesis and its similarity to the dictionary
        title_similarity[thesis] = thesis.title
    return thesis_with_highest_similarity


def find_thesis(info, thesis_data):
    """Looks for an author's name in each element of the info, if the name is unique, the thesis is found, else thesis titles have to be compared.

    Args:
        info: list
        thesis_data: list

    Returns:
        found_thesis: Thesis

    """

    # iterate over each line of the essential info
    for line in info:
        for thesis in thesis_data:
            # pos equals the position of the character of the string, where the substring starts
            author_name = thesis.author.name.split()
            swapped_author_name = author_name[1] + " " + author_name[0]
            # pos equals -1 if the substring doesn't occur; if it doesn't equal 1, the name of the author was found
            # also checks if first and last name are swapped
            if line.find(thesis.author.name) != -1 or line.find(swapped_author_name) != -1:
                if thesis.author.name_unique:
                    thesis.handed_in = True
                    return thesis
                else:
                    current_author = thesis.author.name
                    theses_with_same_author_names = []
                    # fill the above list with all the theses entries that need to be compared
                    for thesis in thesis_data:
                        if thesis.author.name == current_author:
                            theses_with_same_author_names.append(thesis)
                    thesis = compare_titles(info, theses_with_same_author_names)
                    thesis.handed_in = True
                    return thesis
    # if the author name doesn't occur in the exact same way as in the thesis list,
    # search with a tolerance of 1 mistake in the first and in the last name
    for line in info:
        words = line.split()
        for word in words:
            for thesis in thesis_data:
                first_and_last_name = thesis.author.name.split()
                first_name = first_and_last_name[0]
                last_name = first_and_last_name[1]
                if textdistance.hamming(first_name, word) <= 1:
                    for word in words:
                        if textdistance.hamming(last_name, word) <= 1:
                            thesis.handed_in = True
                            return thesis
                elif textdistance.hamming(last_name, word) <= 1:
                    for word in words:
                        if textdistance.hamming(first_name, word) <= 1:
                            thesis.handed_in = True
                            return thesis
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
    print(
        f"{thesis.author.name:20} | {thesis.author.authors_with_this_name} | {unique_str:10} | {thesis.title:50} | "
        f"{thesis.handed_in}")


def print_still_expected_theses(thesis_data):
    """Prints the current entries of the thesis_data list

    Args:
        thesis_data: list

    Returns:

    """

    for thesis in thesis_data:
        print_thesis(thesis)
