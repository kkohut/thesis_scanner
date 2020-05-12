"""This module contains classes that are needed for the assignment of the theses"""

class Thesis:
    def __init__(self, author, title):
        self.author = author
        self.title = title

class Author:
    def __init__(self, name, authors_with_this_name):
        self.name = name
        self.authors_with_this_name = authors_with_this_name