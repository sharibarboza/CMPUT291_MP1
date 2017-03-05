import sys

from connect import get_connection
from constants import BORDER, SELECT
from utils import display_selections, validate_str, validate_num
from queries import insert_user, find_user, user_exists, select, create_tStat, tStat_exists
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

        if not tStat_exists(self.curs):
            create_tStat(self.curs)

        # Keeping track of home page tweets
        self.tweetCurs = None
        self.tweets = None

        self.start_up()
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
        choice = validate_num(SELECT, self.exit, size=len(choices))

        if choice == 1:
    	    self.login()
        elif choice == 2:
    	    self.signup()
        else:
            self.exit()

    def exit(self):
        """Exit from the system and close database"""
        self.curs.close()

        if self.tweetCurs:
            self.tweetCurs.close()

        self.conn.close()
        sys.exit()

    def login(self):
        """Allows returning user to sign in. Will return to the start
        up screen if login fails
        """
        self.username = validate_num("Enter username: ", self.start_up)
        password = validate_str("Enter password: ", self.start_up, 4)
        row = find_user(self.curs, self.username, password)

        if row is None:
            print("Username and/or password not valid.\n")
            self.username = None	
        else:
            name = row[2].rstrip()
            first_name = name.split()[0]
            print("Welcome back, %s." % (first_name))

        if self.username is None:
            self.start_up()
        else:
            self.get_home_tweets()

    def logout(self):
        """Logs user out of the system. Closes all cursors/connections"""
        print("Logged out.")
        self.start_up()

    def signup(self):
        """Creates a new user and inserts user into the database"""
        self.username = self.generate_user()
        name = validate_str("Enter your name: ", self.start_up, 20)
        email = validate_str("Enter your email: ", self.start_up, 15)
        city = validate_str("Enter your city: ", self.start_up, 12)
        timezone = validate_num("Enter your timezone: ", self.start_up, num_type='float')
        password = validate_str("Enter your password: ", self.start_up, 4)

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

    def get_home_tweets(self):
        self.tweets = TweetSearch(self, self.username)
        self.home()

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
            choice = validate_num(SELECT, self.exit, size=len(choices)) - 1

            """
            Main outline for program

            if choices[choice] == 'Select a tweet':
                self.tweets.choose_tweet()
            elif choices[choice] == 'See more tweets':
                more_tweets()
            elif choices[choice] == 'Search tweet':
                search_tweets()
            elif choices[choice] == 'Search users':
                search_users()
            elif choices[choice] == 'Compose tweet':
                compose_tweet()
            elif choices[choice] == 'List followers':
                list_followers()
            elif choices[choice] == 'Manage lists':
                manage_lists()
            elif choices[choice] == 'Logout':
                self.logout()
            """

            # Currently operating functionalties
            if choices[choice] == 'Select a tweet':
                self.tweets.choose_tweet()
            elif choices[choice] == 'Compose tweet':
                compose_tweet(self.conn, self.username, self.home)
            elif choices[choice] == 'Logout':
                self.logout()

   
# ----------------------------------- MAIN --------------------------------------

def main():
    # Log in/sign up user into database
    session = Session()
    conn = session.get_conn()

    # Log out of the database system
    session.logout()

if __name__ == "__main__":
    main()
