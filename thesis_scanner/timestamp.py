""" 
This Script is used to determine the timestamp when the thesis
was submittet
The functions bellow can be used if needed!
by Daniel Rindin
"""

from datetime import datetime

#creates dateTimeObject from current time
dateTimeObj = datetime.now()

def get_timestamp():
    return dateTimeObj

#converts any dateTimeObject to String
def convert_timestamp(datetime):
    try:
        timestampStr = datetime.strftime("%d.%b.%Y (%H:%M)")
        return timestampStr
    except AttributeError:
        raise AttributeError("Wrong Attribute: Not a datetime Object")

#print current timestamp in converted Format
def print_timestamp(datetime):
    str = convert_timestamp(datetime)
    print("Current Timestamp:" , str)

