from datetime import datetime

from constants import BORDER

# Util methods
def convert_date(date_obj):
    """
    Convert a datetime.datetime object from a query into a string
    """
    return datetime.strftime(date_obj, "%b %d %Y")

def display_selections(selections):
    """
    Helper method for easily displaying menus
    param selections: A list containing each menu item
    No need to include numbers in list
    """
    print(BORDER)
    for i, choice in enumerate(selections, 1):
    	print("%d. %s" % (i, choice))
    print(BORDER)

def validate_str(prompt, length=None):
    """
    Used for when user needs to input words
    param length: restricts the number of characters
    commonly used for validating insert values
    """
    valid = False
    usr_input = None

    while not valid:
        usr_input = input(prompt)
        if length and len(usr_input) > length:
            print("Input must be %d characters or less." % (length))
            valid = False
        else:
            valid = True

    return usr_input

def validate_num(prompt, size=None):
    """
    Used for when user needs to input a single number
    Used mainly for menu selections
    param size: specifies range of numbers based on available selections
    """
    valid = False
    choice = None

    while not valid:
        try:
            choice = int(input(prompt))
            if size and choice not in range(1, size+1):
                raise ValueError
        except ValueError:
            if size:
                print("Selection must be a number from 1 to %d." % (size))
            else:
                print("Please enter a number.")
            valid = False
        else:
            valid = True

    return choice

def validate_yn(prompt):
    """
    Used for when prompting the user to enter either y or n
    for yes or no questions
    """
    valid = False
    choice = None
    
    while not valid:
        choice = input(prompt).lower()
        if choice not in ['y', 'n', 'yes', 'no']:
            print("Enter either y/yes or n/no.")
            valid = False
        else:
            valid = True

    return choice