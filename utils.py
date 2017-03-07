from datetime import datetime

from constants import BORDER_LEN, BORDER, BORDER2

# Util methods
def format_string(string, no_border=False):
    """Format string for input"""
    if no_border:
        return "  " + string
    else:
        str1 = "| " + string
        return str1 + " " * (BORDER_LEN - len(str1) + 1) + "|"  

def print_string(string, no_border=False):
    """Prints a string with border lines"""
    print(format_string(string, no_border))

def convert_date(date_obj):
    """Convert a datetime.datetime object from a query into a string
    
    :param data_obj: datetime.datetime object
    """
    return datetime.strftime(date_obj, "%b %d %Y")

def convert_keywords(keywords, lower=True):
    """Takes in string input from user, replaces commas, and converts to list

    :param keywords: list of tokenized strings
    """
    keywords = keywords.replace(',','')
    keywords = keywords.split()

    if lower:
        return [word.lower() for word in keywords]
    else:
        return [word for word in keywords] 

def is_hashtag(term):
    """Return True if term is a hashtag

    :param term: a keyword string
    """
    return term[0] == '#'

def remove_hashtags(keywords):
    """Returns a list with hashtags removed from keywords

    :param keywords: list of tokenized strings
    """
    new_list = []
    for word in keywords:
        if is_hashtag(word):
            word = word.replace('#','')
        new_list.append(word)
    return new_list

def display_selections(selections, title_menu=None):
    """Helper method for easily displaying numbered lists   
 
    param selections: A list containing each menu item
    """
    if title_menu:
        print(BORDER2)
        print_string(title_menu.upper())
        print(BORDER2)

    for i, choice in enumerate(selections, 1):
    	print_string("%d. %s" % (i, choice))
    print(BORDER2)

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
        prompt = format_string(prompt, no_border=True)
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
            prompt = format_string(prompt, no_border=True)
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
        prompt = format_string(prompt, no_border=True)
        choice = input(prompt)
        if choice.lower() not in ['y', 'n', 'yes', 'no']:
            print("Enter either y/yes or n/no.")
            valid = False
        else:
            valid = True

    return choice.lower()
