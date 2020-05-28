"""This module contains functions to extract the date and to check its validity
    Required modules:
    PIL: pip install pillow
	datetime: pip install datetime

    By Melanie Willbold
"""

import re
import datetime
from timestamp import get_timestamp, convert_timestamp, print_timestamp

def get_date(extracted_strings):
    """Filters out the date on the thesis cover

    Args:
        extracted_strings: list
            contains extracted strings of the thesis cover

    Returns:
        datetime:
            date written on the cover

    """
    MONTHS = ["Januar", "Februar", "März", "April", "Mai","Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"]

    # Find numbers in each string
    for line in extracted_strings:
        numbers = re.findall('([0-9]+)', line)
        if 2 <= len(numbers) <= 3:
            # Convert elements to make them comparable
            numbers = [int(n) for n in numbers]
            # Conditions to check if the numbers can be assumed as a date
            if len(numbers) > 2 and 1 <= numbers[0] <= 31 and 1 <= numbers[1] <= 12 and numbers[2] >= 2010:
                return datetime.datetime(numbers[2], numbers[1], numbers[0], 23, 59, 59)
            elif 1 <= numbers[0] <= 31 and numbers[1] >= 2010:
                # Search for month in string and compare it to list of keywords
                for index, month in enumerate(MONTHS, 1):
                    if month in line:
                        return datetime.datetime(numbers[1], index, numbers[0], 23, 59, 59)
    raise RuntimeError("kein Datum gefunden")                   

def test_validity(datetime):
    """Checks validity of the date on the cover

    Args:
        datetime:
            extracted date

    Returns:
        
    """
    today = get_timestamp()
    
    print("Ihr Abgabedatum: " + convert_timestamp(datetime))

    # Check if the date is valid
    if today <= datetime:
        print("True")
    else:
        print("False")