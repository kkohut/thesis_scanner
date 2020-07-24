""" This module can be used to determine if a submitted thesis is already existing.

    Required modules:
    PIL: pip install pillow
	pandas: pip install pandas

    By Melanie Willbold
"""

import math
import collections
import pandas as pd

def string2vec(string):
    """Function to convert a string into a vector

    Args:
        string: str

    Returns:

        tuple:
            count_characters: Counter
            set_characters: set
            length: float
            string: str

    """
    # Count the number of characters in each string
    count_characters = collections.Counter(string)
    # Gets the set of characters and calculates the "length" of the vector
    set_characters = set(count_characters)
    length = math.sqrt(sum(c*c for c in count_characters.values()))
    return count_characters, set_characters, length, string


def cosine_similarity(vector1, vector2, ndigits):
    """Function to calculate the similarity of two vectors

    Args:
        vector1, vector2: tuple
        ndigits: int
            decimal precision can be chosen

    Returns:
        similarity: float
            percentage of similarity with a range from 0 to 1

    """
    # Get the common characters between the two character sets
    common_characters = vector1[1].intersection(vector2[1])
    # Sum of the product of each intersection character
    product_summation = sum(vector1[0][character] * vector2[0][character] for character in common_characters)
    # Gets the length of each vector from the string2vec output
    length = vector1[2] * vector2[2]
    # Calculates cosine similarity and rounds the value to ndigits decimal places
    if length == 0:
        # Set value to 0 if string is empty
        similarity = 0
    else:
        similarity = round(product_summation/length, ndigits)
    return similarity


def find_similar_thesis(thesis_list, thesis_title, ndigits):
    """ Finds the thesis title with the highest similarity score

    Args:
        thesis_list: list
            list with already existing thesis titles
        thesis_title: str
            submitted thesis
        ndigits: int
            decimal precision can be chosen

    Returns:
        results_df: DataFrame 
            table contains submitted title, thesis title with the highest similarity and the similarity score between both

    """
    highest_similarity = 0
    results_list = []

    # Apply string2vec function to already existing titles and to thesis title to be compared
    vector_list = [string2vec(str(i)) for i in thesis_list]
    thesis_vector = string2vec(thesis_title)

    # Compare title with each title in the list
    for i in range(len(vector_list)):
        vector = vector_list[i]
        # Calculate cosine similarity
        similarity_score = cosine_similarity(thesis_vector, vector, ndigits)
        if highest_similarity <= similarity_score:
            highest_similarity = similarity_score
            thesis_with_hightest_similarity = vector[3]
    
    results_list.append([thesis_title, thesis_with_hightest_similarity, highest_similarity])
    
    # Convert results to dataframe
    results_df = pd.DataFrame(results_list, columns=['thesis_title', 'similar_title', 'similarity_score'])
    
    return results_df