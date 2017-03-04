import sys

from connect import get_connection
from constants import BORDER, SELECT
from utils import display_selections, validate_str, validate_num
from queries import insert_user, find_user, user_exists, select, create_tStat
from tweet import TweetSearch, compose_tweet

"""
CMPUT 291 Mini Project 1
Contributors: Hong Zhou, Haotian Zhu, Sharidan Barboza
Due: March 12 5 PM
"""

class Session:

    def __init__(self):
        """Establishes a connection with cx_Oracle and logs in user"""
 
        self.username = None	    
        self.conn = get_connection("sql_login.txt")
        self.curs = self.conn.cursor()
        create_tStat(self.curs)

        # Keeping track of home page tweets
        self.tweetCurs = None
        self.tweets = None
        
    def get_conn(self):
        """Return the connection"""
        return self.conn

    def get_curs(self):
        """Return the cursor"""
        return self.curs

    def get_username(self):
        """Return the logged in user id"""
        return self.username

    def start_up(self):
        """Displays start up screen to provide options for both
        registered and unregistered users 
        """
        choices = ["Login", "Sign up", "Exit"]
        display_selections(choices)
        choice = validate_num(SELECT, size=len(choices))

        if choice == 1:
    	    self.login()
        elif choice == 2:
    	    self.signup()
        else:
            self.conn.close()
            sys.exit()

    def login(self):
        """Allows returning user to sign in. Will return to the start
        up screen if login fails
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
            self.tweets = TweetSearch(self, self.username)

        if self.username is None:
            self.start_up()

    def logout(self):
        """Logs user out of the system. Closes all cursors/connections"""
        self.curs.close()

        if self.tweetCurs:
            self.tweetCurs.close()

        print("Logged out.")
        main()

    def signup(self):
        """Creates a new user and inserts user into the database"""
        self.username = self.generate_user()
        name = validate_str("Enter your name: ", 20)
        email = validate_str("Enter your email: ", 15)
        city = validate_str("Enter your city: ", 12)
        timezone = float(validate_num("Enter your timezone: "))
        password = validate_str("Enter your password: ", 4)

        print("Welcome %s! Your new user id is %d.\n" % (name, self.username))

        data = [self.username, password, name, email, city, timezone]
        insert_user(self.conn, data)

    def generate_user(self):
        """Generates a new unique user id for user sign-up"""
        select(self.curs, 'users')
        rows = self.curs.fetchall()
        new_usr = len(rows) + 1
    
        while user_exists(self.curs, new_usr): 
            new_usr += 1
        return new_usr

    def main_menu(self):
        """Displays the main functionality menu
    
        :param curs: cursor object
        """
        choices = [
            "Search tweets", 
            "Search users", 
            "Compose tweet", 
            "List followers", 
            "Manage lists",
            "Logout"
        ]

        # Allow tweet selection if user has any tweets
        if self.tweetCurs:
            choices.insert(0, "Select a tweet")

            rows = self.tweetCurs.fetchmany(5)
            if len(rows) > 0:
                choices.insert(1, "See more tweets")
    
        display_selections(choices)
        return choices

    def home(self):
    # Display main system functionalities menu
        while True:
            print(BORDER)
            self.tweetCurs = self.tweets.get_user_tweets()
            choices = self.main_menu()
            choice = validate_num(SELECT, size=len(choices)) 

            """
            Main outline for program
            if choice == 1:
                self.tweets.select_tweet()
            elif choice == 2:
                more_tweets()
            elif choice == 3:
                search_tweets()
            elif choice == 4:
                search_users()
            elif choice == 5:
                compose_tweet()
            elif choice == 6:
                list_followers()
            elif choice == 7:
                manage_lists(session)
            elif choice == 8:
                more_tweets()
            """

            # Currently operating functionalties
            if choice == 1:
                self.tweets.select_tweet()
            elif choice == 5:
                compose_tweet(self.conn, self.username)
            elif choice == 8:
                self.logout()

   
# ----------------------------------- MAIN --------------------------------------

def main():
    # Log in/sign up user into database
    session = Session()
    session.start_up()
    conn = session.get_conn()
    
    session.home()

    # Log out of the database system
    session.logout()

if __name__ == "__main__":
    main()
