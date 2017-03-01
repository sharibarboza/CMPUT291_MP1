import sys

from connect import get_connection
from constants import BORDER, SELECT
from utils import display_selections
from validate import validate_num, validate_str

def get_user(conn):
    choices = ["Login", "Sign up", "Exit"]
    display_selections(choices)
    choice = validate_num(SELECT, size=len(choices))

    username = None

    if choice == 1:
    	username = login(conn)
    elif choice == 2:
    	username = signup(conn)
    else:
        sys.exit()

    if username:
    	return username
    else:
    	get_user(conn)

def login(conn):
    print(BORDER)
    username = validate_num("Enter username: ")
    password = input("Enter password: ")

    curs = conn.cursor()
    named_params = {'u': username, 'p': password}
    curs.execute('SELECT * FROM users WHERE usr=:u AND pwd=:p', named_params)
    row = curs.fetchone()

    if row is None:
    	print("Username and/or password is not valid.\n")
    	return None
    else:
    	print("Welcome back, %s." % (row[2].rstrip()))
    	return username

    return username

def signup(conn):
    print(BORDER)
    name = validate_str("Enter your name: ", 20)
    email = validate_str("Enter your email: ",15)
    city = validate_str("Enter your city: ",12)
    timezone = validate_num("Enter your timezone: ")
    password = validate_str("Enter your password: ",4)

    return ""

# ----------------------------------- MAIN --------------------------------------

def main():
    # Connect to database
    conn = get_connection("sql_login.txt")

    # Opening screen
    username = get_user(conn)

if __name__ == "__main__":
	main()
