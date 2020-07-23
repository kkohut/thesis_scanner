"""
this script is a unittest script to the "timsestamp.py" script 
by Daniel Rindin
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'thesis_scanner'))

from datetime import datetime
import timestamp , unittest


class TestTimestampMethods(unittest.TestCase):

    #test for get_timestamp not needed

    def test_convert_timestamp_exception(self):
        isOk = False
        try:
            timestamp.convert_timestamp(None)
        except AttributeError:
            isOk = True

        self.assertTrue(isOk)

    #creates TestTimestampObj for 15.Sep.2020 (16:25) and converts it to string
    def test_convert_timestamp_(self):
        testTimestampObj = datetime(2020,9,15,16,25)
        self.assertEqual(timestamp.convert_timestamp(testTimestampObj),"15.Sep.2020 (16:25)")
    
    def test_print_timestamp_exception(self):
        isOk = False
        try:
            timestamp.print_timestamp(None)
        except AttributeError:
            isOk = True

        self.assertTrue(isOk)
    
if __name__ == '__main__':
    unittest.main()