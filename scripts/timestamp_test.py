import timestamp
"""
WORK IN PROGRESS
this script will be a test script to the "timsestamp.py" script 
by Daniel Rindin
"""
def test():
    timestampObj = timestamp.get_timestamp()
    str = timestamp.convert_timestamp(timestampObj)
    print(str)

def test_print_timestamp():
    timestamp.print_timestamp()

test_print_timestamp()
test()