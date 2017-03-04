import sys

from connect import get_connection
from constants import BORDER, SELECT
from tweet import TweetSearch, compose_tweet

from utils import (
    display_selections,
    validate_str,
    validate_num
) 

from queries import (
    insert_user,
    find_user,
    user_exists,
    select,
    create_tStat
)

class Session:

    def __init__(self, conn):
        self.conn = conn
        self.curs = conn.cursor()
        self.username = None

        self._start_up()
        self.tweets = TweetSearch(self, self.username)
        create_tStat(self.conn.cursor())

    def _start_up(self):
        """
        Gets the id of the logged in user
        Will be from an existing user or a newly signed-up user
        """
        choices = ["Login", "Sign up", "Exit"]
        display_selections(choices)
        choice = validate_num(SELECT, size=len(choices))

        if choice == 1:
    	    self.login()
        elif choice == 2:
    	    self.signup()
        else:
            sys.exit()

    def get_conn(self):
        return self.conn

    def login(self):
        """
        Allows returning user to sign in
        """
        self.username = validate_num("Enter username: ")
        password = input("Enter password: ")
        row = find_user(self.curs, self.username, password)

        if row is None:
            print("Username and/or password not valid.\n")
            self.username = None	
        else:
    	    name = row[2].rstrip()
    	    first_name = name.split()[0]
    	    print("Welcome back, %s." % (first_name))

        if self.username is None:
            self._start_up()

    def signup(self):
        """
        Creates a new user
        """
        name = validate_str("Enter your name: ", 20)
        email = validate_str("Enter your email: ", 15)
        city = validate_str("Enter your city: ", 12)
        timezone = validate_num("Enter your timezone: ")
        password = validate_str("Enter your password: ", 4)

        self.username = self.generate_user()
        print("Welcome %s! Your new user id is %d.\n" % (name, self.username))

        data = [self.username, password, name, email, city, timezone]
        insert_user(self.conn, data)

    def generate_user(self):
        """
        Generates a new unique user id
        """
        select(self.curs, 'users')
        rows = self.curs.fetchall()
        new_usr = len(rows) + 1
    
        while user_exists(self.curs, new_usr): 
            new_usr += 1
    
        return new_usr

    def home(self):
        """
        Displays 5 tweets from users who are being followed
        """
        print(BORDER)
        self.curs = self.tweets.get_user_tweets()
        choices = self._main_menu(self.curs)

        choice = validate_num(SELECT, size=len(choices)) 

        """
        if choice == 1:
            search_tweets()
        elif choice == 2:
            search_users()
        elif choice == 3:
            compose_tweet()
        elif choice == 4:
            get_followers()
        elif choice == 5:
            manage_lists()
        elif choice == 7:
            select_tweet(curs)
        elif choice == 8:
            more_tweets()
        """
        if choice == 3:
            choice = compose_tweet(self.username)
        elif choice == 7:
            choice = self.tweets.select_tweet()

        return choice
       
    def _main_menu(self, curs):
        """
        Displays the main functionality menu for the home screen
        """
        choices = [
            "Search tweets",
            "Search users",
            "Compose tweet",
            "List followers",
            "Manage lists",
            "Logout"
        ]

        if curs:
            choices.append("Select a tweet")
            rows = curs.fetchmany(5)

            if (len(rows) > 0):
                choices.append("See more tweets")

        display_selections(choices)
        return choices

    def logout(self):
        """
        Close cursors and connections
        Exit program
        """
        self.curs.close()
        self.conn.close()
        print("Logged out.")
        sys.exit()
        

# ----------------------------------- MAIN --------------------------------------

def main():
    # Connect to database
    conn = get_connection("sql_login.txt")
    s = Session(conn)

    # Opening screen
    choice = ""
    while choice != 6:
        choice = s.home()

    s.logout()

if __name__ == "__main__":
    main()
