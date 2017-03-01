# Input validation methods

def validate_str(prompt):
    """
    Used for when user needs to input words
    Ensures that user input is non-empty
    """
    usr_input = ""
    while len(usr_input) == 0:
    	usr_input = input(prompt)
    return usr_input

def validate_num(prompt, size=None):
    """
    Used for when user needs to input a single number 
    Used mainly for menu selections
    """
    valid = False
    while not valid:
        try:
            choice = int(input(prompt))
            if size and choice not in range(1, size + 1):
            	raise ValueError
        except ValueError:
        	if size:
        		print("Selection must be a number from 1 to %d." % (size))
        	else:
        		print("Please enter a number.")
        	valid = False
        else:
            return choice
