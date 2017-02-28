from constants import BORDER

# Util methods 

def display_selections(selections):
    print(BORDER)
    for i, choice in enumerate(selections, 1):
    	print("%d. %s" % (i, choice))
    print(BORDER)