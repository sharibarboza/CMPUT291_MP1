import sys

from connect import get_connection
from utils import display_selections
from validate import get_selection

def get_user(conn):
	choices = ["Login", "Sign up", "Exit"]
	display_selections(choices)
	choice = get_selection(len(choices))

	username = None

	if choice == 3:
		sys.exit()

	return ""

# ----------------------------------- MAIN --------------------------------------

def main():
    # Connect to database
    conn = get_connection("sql_login.txt")

    # Opening screen
    username = get_user(conn)

if __name__ == "__main__":
	main()
