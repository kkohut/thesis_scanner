"""This module contains classes that are needed for the assignment of the theses"""

"""
    By Kevin Kohut
"""
class Thesis:
    def __init__(self, author, title):
        self.author = author
        self.title = title
        self.handed_in = False

class Author:
    def __init__(self, name, authors_with_this_name, name_unique):
        self.name = name
        self.authors_with_this_name = authors_with_this_name
        self.name_unique = name_unique