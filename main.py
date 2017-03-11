import sys

from connect import get_connection
from utils import *
from queries import * 
from tweet import TweetSearch, compose_tweet, search_tweets
from user import UserSearch, search_users, list_followers 
from mlist import ListManager 

"""
CMPUT 291 Mini Project 1
Contributors: Hong Zhou, Haotian Zhu, Sharidan Barboza
Due: March 12 5 PM
"""

class Twitter:

    def __init__(self):
        """Establishes a connection with cx_Oracle and logs in user"""
        self.conn = self.connect() 
        self.curs = self.conn.cursor()
        self.username = None
        self.name = None
        self.tweets = None
        self.s_tweets = None
        self.current = None
        self.lists = None 

        create_tStat(self.curs)
        create_uStat(self.curs)

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
        """Returns the cursor"""
        return self.curs

    def get_username(self):
        """Return the logged in user id"""
        return self.username

    def get_name(self):
        """Return the user's first and last name"""
        return self.name

    def get_current(self):
        """Get the current functionality"""
        return self.current

    def start_up(self):
        """Displays start up screen to provide options for both
        registered and unregistered users 
        """
        width = 60
        print_border(width, True)
        print_string("            WELCOME TO THE TWITTER DATABASE", length=width)
        print_string(" Created by: Hong Zhou, Haotion Zhu, and Sharidan Barboza", length=width)
        print_border(width, True, sign='|')
        print_string("            1. Login   2. Sign-Up   3. Exit", length=width)
        print_border(width, False, sign='|')
        print_string("INPUT INSTRUCTIONS:", length=width) 
        print_string("Enter a number specified by the menu to select an option.", length=width) 
        print_string("Enter control-C any time to immediately exit the program.", length=width)
        print_string("Enter q, quit, or exit to cancel input and go back.", length=width)
        print_border(width, True)
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
        print("\nThank you for using Twitter. Closing the database ...")

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
            print("Username and/or password not valid.\n")
            self.username = None
        else:
            self.name = row[2].rstrip()
            self.lists = ListManager(self)	

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
        timezone = validate_num("Enter your timezone: ", self, self.start_up, num_type='float', rnge=(-12,14))
        password = validate_str("Enter your password: ", self, self.start_up, 4)
        self.name = name

        print_border(50, False)
        print("Name: %s, Email: %s, City: %s, Timezone: %d" % (name, email, city, timezone))
        confirm = validate_yn("Confirm user? y/n: ", self)

        if confirm in ["y", "yes"]:
            print("Welcome %s! Your username is %d." % (name, self.username))
            data = [self.username, password, name, email, city, timezone]
            insert_user(self.conn, data)
            press_enter(self)
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
        self.tweets = TweetSearch(self)
        self.current = self.tweets
        self.tweets.get_user_tweets()
        self.home()

    def _main_menu(self):
        """Displays the main functionality menu
    
        :param t: TweetSearch object (can be self.tweets or self.s_tweets)
        """
        choices = []
        category = self.current.get_category()

        # Allow tweet selection if user has any tweets
        if self.current.results_exist():
            choices.insert(0, "Select a result")
    
            if self.current.more_results_exist():
                choices.insert(1, "See more results")

        if self.current.is_search():
            choices.append("Do another search")

        if category == "Home": 
            main_list = [
                "Search tweets", 
                "Search users", 
                "Compose tweet",
                "List followers", 
                "Manage lists"
            ]
            choices.extend(main_list)
   
        home_screen = False 
        if category == "Home":
            home_screen = self.current.is_first_page() 
        if not home_screen or category != "Home": 
            choices.append("Home")
        choices.append("Logout")

        display_selections(choices, no_border=True)
        return choices

    def home(self, current=None, reset=True):
        """Displays main system functionalities menu"""
        if current is None:
            self.current = self.tweets
        else:
            self.current = current

        if reset:
            self.current = self.current.reset()

        while True:          
            print_newline()

            self.current.display_results()
            choices = self._main_menu()
            choice = validate_num(SELECT, self, self.start_up, size=len(choices)) - 1
            option = choices[choice]

            category = self.current.get_category()

            # Currently operating functionalties
            if option == 'Select a result':
                self.current.choose_result()
                self.current = self.tweets
            elif option == 'See more results':
                self.current.more_results()
            elif option == 'Search tweets':
                self.current = search_tweets(self)
            elif category == 'TweetSearch' and option == 'Do another search':
                self.current = search_tweets(self)
            elif option == 'Search users':
                self.current = search_users(self) 
            elif category == 'UserSearch' and option == 'Do another search':
                self.current = search_users(self)
            elif option == 'Compose tweet':
                compose_tweet(self)
            elif option == 'List followers':
                self.current = list_followers(self)
            elif option == 'Manage lists':
                self.lists.manage_lists() 
            elif option == "Home":
                self.current = self.tweets
                self.home()
            elif option == 'Logout':
                self.logout()
   
# ----------------------------------- MAIN --------------------------------------

def main():
    # Log in/sign up user into database
    twitter = Twitter()
    conn = twitter.get_conn()

    # Log out of the database system
    session.logout()

if __name__ == "__main__":
    main()
