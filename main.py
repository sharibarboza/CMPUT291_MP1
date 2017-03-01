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
        print("Username and/or password not valid.\n")
        username = None	
    else:
    	print("Welcome back, %s." % (row[2].rstrip()))

    return username

def signup(conn):
    print(BORDER)
    name = validate_str("Enter your name: ", 20)
    email = validate_str("Enter your email: ", 15)
    city = validate_str("Enter your city: ", 12)
    timezone = validate_num("Enter your timezone: ")
    password = validate_str("Enter your password: ", 4)

    username = get_new_user(conn)
    print("Welcome %s!\n" % (name))

    data = [username, password, name, email, city, timezone]
    cursInsert = conn.cursor()
    cursInsert.execute("INSERT INTO users(usr,pwd,name,email,city,timezone)"
        "VALUES (:1,:2,:3,:4,:5,:6)", data)
    conn.commit()
 
    return username 

def get_new_user(conn):
    curs = conn.cursor()
    curs.execute('SELECT usr FROM users')
    rows = curs.fetchall()
    new_usr = len(rows) + 1
    
    while user_exists(new_usr, curs): 
        new_usr += 1
    
    return new_usr

def user_exists(user, curs):
    curs.execute('SELECT usr FROM users WHERE usr=:1', [user])
    return curs.fetchone() is not None 


# ----------------------------------- MAIN --------------------------------------

def main():
    # Connect to database
    conn = get_connection("sql_login.txt")

    # Opening screen
    username = get_user(conn)

if __name__ == "__main__":
    main()
