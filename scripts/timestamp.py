from datetime import datetime
""" 
This Script is used to determine the timestamp when the thesis
was submittet
The functions bellow can bes used if needed!
by Daniel Rindin
"""

#creates dateTimeObject from current time
dateTimeObj = datetime.now()

def get_timestamp():
    return dateTimeObj

#converts any dateTimeObject to String
#MISSING: Exception when input is a Wrong Object
def convert_timestamp(obj):
    timestampStr = obj.strftime("%d.%b.%Y (%H:%M)")
    return timestampStr

#print current timestamp in converted Format
def print_timestamp():
    print("Current Timestamp:" , convert_timestamp(dateTimeObj))

