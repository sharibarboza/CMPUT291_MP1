from constants import BORDER

# Util methods 

def display_selections(selections):
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
        in length and len(usr_input) > length:
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
