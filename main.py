import sys

from connect import get_connection
from constants import BORDER, SELECT
from utils import *
from queries import * 
from tweet import TweetSearch, compose_tweet, search_tweets

"""
CMPUT 291 Mini Project 1
Contributors: Hong Zhou, Haotian Zhu, Sharidan Barboza
Due: March 12 5 PM
"""

class Session:

    def __init__(self):
        """Establishes a connection with cx_Oracle and logs in user"""
        self.conn = self.connect() 
        self.curs = self.conn.cursor()
        self.username = None
        self.logged_user = None
        self.name = None
        self.tweets = None
        self.s_tweets = None      

        if not tStat_exists(self.curs):
            create_tStat(self.curs)

        self.start_up()

    def connect(self):
        """ Get connection with filename 
        File should include username and password to log into Oracle
        """
        if len(sys.argv) > 1:
            return get_connection(sys.argv[1])
        else:
            return get_connection('sql_login.txt')
        
    def get_conn(self):
        """Return the connection"""
        return self.conn

    def get_curs(self):
        """Return the cursor"""
        return self.curs

    def get_username(self):
        """Return the logged in user id"""
        return self.username

    def get_name(self):
        """Return the user's first and last name"""
        return self.name

    def start_up(self):
        """Displays start up screen to provide options for both
        registered and unregistered users 
        """
        print(BORDER2)
        print_string("WELCOME TO TWITTER - A COMMAND LINE CLIENT")
        print_string("Created by: Hong Zhou, Haotion Zhu, and Sharidan Barboza")
        print(BORDER2)
        choices = ["Login", "Sign-Up", "Exit"]
        display_selections(choices)
        print_string("INPUT INSTRUCTIONS:") 
        print_string("Enter a number specified by the menu to select an option.") 
        print_string("Enter control-C any time to immediately exit the program.")
        print_string("Enter q, quit, or exit to cancel input and return to the previous screen.")
        print(BORDER)
        choice = validate_num(SELECT, self, self.exit, size=3)

        if choice == 1:
    	    self.login()
        elif choice == 2:
    	    self.signup()
        else:
            self.exit()

        self.get_home_tweets()

    def exit(self):
        """Exit from the system and close database"""
        print("\nThank you for using Twitter. Existing database ...")

        self.curs.close()
        self.conn.close()
        sys.exit()

    def login(self):
        """Allows returning user to sign in. Will return to the start
        up screen if login fails
        """
        self.username = validate_num("Enter username: ", self, menu_func=self.start_up)
        password = validate_str("Enter password: ", self, self.start_up, 4)
        row = find_user(self.curs, self.username, password)

        if row is None:
            print_string("Username and/or password not valid.\n")
            self.username = None
        else:
            self.name = row[2].rstrip()
            self.logged_user = "Logged in: %d (%s)" % (self.username, self.name)	

        if self.username is None:
            self.start_up()

    def logout(self):
        """Logs user out of the system. Returns user to start up screen"""
        self.start_up()

    def signup(self):
        """Creates a new user and inserts user into the database"""
        self.username = self.generate_user()
        name = validate_str("Enter your name: ", self, self.start_up, 20)
        email = validate_str("Enter your email: ", self, self.start_up, 15)
        city = validate_str("Enter your city: ", self, self.start_up, 12)
        timezone = validate_num("Enter your timezone: ", self, self.start_up, num_type='float')
        password = validate_str("Enter your password: ", self, self.start_up, 4)

        print(BORDER)
        print("Name: %s, Email: %s, City: %s, Timezone: %d" % (name, email, city, timezone))
        confirm = validate_yn("Confirm user? y/n: ", self)

        if confirm in ["y", "yes"]:
            print("Welcome %s! Your new user id is %d." % (name, self.username))
            data = [self.username, password, name, email, city, timezone]
            insert_user(self.conn, data)
            press_enter()
        else:
            self.start_up()

    def generate_user(self):
        """Generates a new unique user id for user sign-up"""
        select(self.curs, 'users')
        rows = self.curs.fetchall()
        new_usr = len(rows) + 1
    
        while user_exists(self.curs, new_usr): 
            new_usr += 1
        return new_usr

    def get_home_tweets(self):
        """Gets the tweets of users being followed by the user"""
        self.tweets = TweetSearch(self, self.username)
        self.tweets.get_user_tweets()
        self.home()

    def _main_menu(self, t):
        """Displays the main functionality menu
    
        :param t: TweetSearch object (can be self.tweets or self.s_tweets)
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
        if t.tweets_exist():
            choices.insert(0, "Select a tweet")
    
            if t.more_tweets_exist():
                choices.insert(1, "See more tweets")
    
        display_selections(choices, "Main Menu")
        return choices

    def home(self):
        """Displays main system functionalities menu"""
        while True:          
            t = self.s_tweets if self.s_tweets else self.tweets
            
            if self.s_tweets:
                title = "SEARCH RESULTS FOR %s" % (self.s_tweets.get_searched().upper())
            else: 
                title = "HOME"
            
            print('\n' + BORDER2)
            split_title(title, self.logged_user)
            print(BORDER2)

            t.display_tweets()
            choices = self._main_menu(t)
            choice = validate_num(SELECT, self, self.start_up, size=len(choices)) - 1
            option = choices[choice]

            if self.s_tweets and option not in ['Select a tweet', 'See more tweets']:
                self.s_tweets = None

            """
            Main outline for program

            if option  == 'Select a tweet':
                self.tweets.choose_tweet()
            elif option == 'See more tweets':
                more_tweets()
            elif option == 'Search tweets':
                search_tweets()
            elif option == 'Search users':
                search_users()
            elif option == 'Compose tweet':
                compose_tweet()
            elif option == 'List followers':
                list_followers()
            elif option == 'Manage lists':
                manage_lists()
            elif option == 'Logout':
                self.logout()
            """

            # Currently operating functionalties
            if option == 'Select a tweet':
                t.choose_tweet()
            elif option == 'See more tweets':
                t.more_tweets()
            elif option == 'Search tweets':
                self.s_tweets = search_tweets(self, self.username) 
            elif option == 'Compose tweet':
                compose_tweet(self, self.username, menu_func=self.home)
            elif option == 'Logout':
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
