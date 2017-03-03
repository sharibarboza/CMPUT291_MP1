import sys

from connect import get_connection
from constants import BORDER, SELECT
from tweet import TweetSearch

from utils import (
    display_selections,
    validate_str,
    validate_num
) 

from queries import (
    insert_user,
    get_user,
    user_exists,
    select
)

def start_up(conn):
    """
    Gets the id of the logged in user
    Will be from an existing user or a newly signed-up user
    """
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
    	start_up(conn)

def login(conn):
    """
    Allows returning user to sign in
    """
    print(BORDER)
    username = validate_num("Enter username: ")
    password = input("Enter password: ")

    curs = conn.cursor()
    row = get_user(curs, username, password)

    if row is None:
        print("Username and/or password not valid.\n")
        username = None	
    else:
    	name = row[2].rstrip()
    	first_name = name.split()[0]
    	print("Welcome back, %s." % (first_name))

    return username

def signup(conn):
    """
    Creates a new user
    """
    print(BORDER)
    name = validate_str("Enter your name: ", 20)
    email = validate_str("Enter your email: ", 15)
    city = validate_str("Enter your city: ", 12)
    timezone = validate_num("Enter your timezone: ")
    password = validate_str("Enter your password: ", 4)

    username = get_new_user(conn)
    print("Welcome %s!\n" % (name))

    data = [username, password, name, email, city, timezone]
    insert_user(conn, data)

    return username 

def get_new_user(conn):
    """
    Generates a new unique user id
    """
    curs = conn.cursor()
    select(curs, 'users')
    rows = curs.fetchall()
    new_usr = len(rows) + 1
    
    while user_exists(curs, new_usr): 
        new_usr += 1
    
    return new_usr

# ----------------------------------- MAIN --------------------------------------

def main():
    # Connect to database
    conn = get_connection("sql_login.txt")

    # Opening screen
    logged_user = start_up(conn)

    # Display user's opening screen
    user_tweets = TweetSearch(conn, logged_user)

if __name__ == "__main__":
    main()
