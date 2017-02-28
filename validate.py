from constants import SELECT

# Input validation methods

def get_input(prompt):
	"""
	Used for when user needs to input words
	Ensures that user input is non-empty
	"""
	usr_input = ""
	while len(usr_input) == 0:
		usr_input = input(prompt)
		
	return usr_input

def get_selection(size):
	"""
	Used for when user needs to input a single number
	Used mainly for menu selections
	"""
	valid = False

	while not valid:
		try:
			choice = int(input(SELECT))
			if choice not in range(1, size + 1):
				raise ValueError
		except ValueError:
			print("Selection must be a number from 1 to %d." % (size))
			valid = False
		else:
			return choice
