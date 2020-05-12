"""This module contains several functions to analyze and categorize data from a string"""

import os
import pytesseract , text_extraction
#from names_dataset import NameDataset -- not used
#import text_extraction

def read_thesis_data(file):
    """Reads data about each expected thesis from a .txt file and stores it in a dictionary

    Args:
        file: str

    Returns:
        author_data: dict

    """
    thesis_data = {}
    with open(file, "r") as f:
        for line in f:
            # seperates author and title which should be seperated by a comma
            info_splits = line.split(",")   
            # removes '\n' and spaces at start and end of the string
            author = info_splits[0].strip() 
            title = info_splits[1].strip()
            # stores author and the title of his or her thesis as a key:value pair in a dictionary  
            thesis_data[author] = title     
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

def find_author_and_title(info, thesis_data): # tolerance still needed
    """Looks for an author's name in each element of the info

    Args:
        info: list
        authors: list

    Returns:
        author: str

    """
                        
    # iterate over each line of the essential info
    for element in info:
        for author in thesis_data:
            # pos equals the position of the character of the string, where the substring starts
            pos = element.find(author)
            # pos equals -1 if the substring doesn't occur; if it doesn't equal 1, the name of the author was found
            if pos != -1:                   
                title = thesis_data[author]
                del thesis_data[author]
                return author, title
    # if none of the expected authors occurs return None    
    return None