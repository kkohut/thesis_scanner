"""This module contains functions to get the deadline and check the validity of the submission"""

import re
import datetime
from timestamp import get_timestamp, convert_timestamp, print_timestamp

def get_deadline(text):

    #keywords if the month has been written-out
    date_keywords = ["Januar", "Februar", "März", "April", "Mai","Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"]
    #find values of the date
    digets = re.findall('([0-9]+)', text)
    #if three numbers were found, put them in the right order and convert to a datetime-object
    if len(digets) > 2:
        deadline = datetime.datetime(int(digets[2]),int(digets[1]),int(digets[0]),23,59,59)
    #if only two numbers were found search for month in text
    else:
        for month in date_keywords:
            if re.search(month, text):
                 for i in range(0,12):
                      if month == date_keywords[i]:
                           #replace the value of month with a digit and convert to a datetime-object
                           new_month = i+1
                           deadline = datetime.datetime(int(digets[1]), new_month, int(digets[0]),23,59,59)
                           break
    
    return deadline

def test_validity(datetime):

    today = get_timestamp()

    print("Ihre Abgabefrist endet am: " + convert_timestamp(datetime))

    #check if the deadline was exceeded
    if today <= datetime:
        print("Die Abgabe war gueltig.")
    else:
        print("Die Frist wurde ueberschritten. Ihre Abgabe ist ungueltig.")

            