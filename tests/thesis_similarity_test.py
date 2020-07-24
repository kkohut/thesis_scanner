"""This test module tests the cosine similarity function of the thesis_similarity.py module"""

"""
    By Melanie Willbold
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'thesis_scanner'))

import math
import collections
from thesis_similarity import string2vec, cosine_similarity

class TestThesisSimilarity(unittest.TestCase):
    
    def test_cosineSimilarity(self):

        text = "Hallo"
        self.assertEqual(cosine_similarity(string2vec(text), string2vec(text), 0), 1.0)
        self.assertEqual(cosine_similarity(string2vec(text), string2vec(""), 0), 0.0)


if __name__ == '__main__':
    unittest.main()