from datetime import datetime

from constants import BORDER

# Util methods
def convert_date(date_obj):
    """Convert a datetime.datetime object from a query into a string
    
    :param data_obj: datetime.datetime object
    """
    return datetime.strftime(date_obj, "%b %d %Y")

def display_selections(selections):
    """Helper method for easily displaying numbered lists   
 
    param selections: A list containing each menu item
    """
    print(BORDER)
    for i, choice in enumerate(selections, 1):
    	print("%d. %s" % (i, choice))
    print(BORDER)

def check_quit(user_input):
    """Checks if a user entered a quit message

    :param: user_input: input from the user
    """
    return user_input.lower() in ['quit', 'q', 'exit']

def exit_input(choice, menu_func):
    """Determines what to return when a user quits an input prompt
    
    :param menu_func: the function to return to
    :param choice: the user input
    """
    if menu_func is None:
        return choice
    else:
        return menu_func()

def press_enter(prompt="Press Enter to continue."):
    """Requires user to press enter key before continuing

    :param: string message
    """
    input(prompt)

def validate_str(prompt, menu_func=None, length=None):
    """Used for when user needs to input words
    Commonly used for validating insert values  
    If you are passing a function name, make sure to not put () so it won't be called
 
    :param prompt: string message
    :param menu_func: if user enters quit, return to this function
    :param length (optional): restricts the number of characters
    """
    valid = False
    usr_input = None

    while not valid:
        usr_input = input(prompt)
        if check_quit(usr_input):
            exit_input(usr_input, menu_func) 
        if length and len(usr_input) > length:
            print("Input must be %d characters or less." % (length))
            valid = False
        else:
            valid = True

    return usr_input

def validate_num(prompt, menu_func=None, size=None, num_type='int'):
    """Used for when user needs to input a single number
    Used mainly for menu selections
    If you are passing a function name, make sure to not put () so it won't be called
    
    :param prompt: string message
    :param menu_func: if user enters quit, return to this function
    :param size (optional): specifies range of numbers based on available selections
    :param num_type (optional): validate either integer or float (default: integer) 
    """
    assert(num_type=='int' or num_type=='float'), "type must be either int or float"

    valid = False
    choice = None

    while not valid:
        try:
            choice = input(prompt)
            if check_quit(choice):
                exit_input(choice, menu_func) 
            if num_type == 'int':
                choice = int(choice)
            else:
                choice = float(choice)
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

    if num_type == 'int':
        return int(choice)
    else:
        return float(choice)

def validate_yn(prompt):
    """Used for when prompting the user to enter either y/yes or n/no
    
    :param prompt: string message
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
