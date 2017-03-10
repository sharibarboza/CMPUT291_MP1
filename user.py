from queries import *
from utils import *
from tweet import Tweet

def search_users(session):
    """Matches users/cities to keywords

    :param session: Session object
    """
    search_input = validate_str("Enter keyword for user search: ", session, session.home, null=False)
    s_users = UserSearch(session, keywords=search_input)
    s_users.get_results()
    return s_users


def list_followers(session):
    """Gets the user's followers"""
    f_users = UserSearch(session, followers=True)
    f_users.get_follows() 
    return f_users


class User:

    def __init__(self, session, data):
        self.session = session
        self.conn = session.get_conn()
        self.curs = session.get_curs()
        self.logged_user = session.get_username()
        
        self.id = data[0]
        self.pwd = data[1]
        self.name = data[2].rstrip()
        self.email = data[3].rstrip()
        self.city = data[4].rstrip()
        self.timezone = data[5]
        self.tz_str = convert_timezone(self.timezone)

        self.rows = get_user_stats(self.curs, self.id)
        self.following = self.rows[0][1]
        self.followers = self.rows[0][2]
        self.num_tweets = self.rows[0][3]

        self.index = 3
        self.all_tweets = [] 
        self.tweets = []
        self.more_exist = False
        self.get_tweets()

    def user_menu(self):
        choices = ["Follow", "Go back", "Do another search", "Home", "Logout"]
        if self.more_exist:
            choices.insert(1, "See more tweets")

        print_border(thick=True)
        display_selections(choices)

        return choices

    def get_tweets(self):
        get_user_tweets(self.curs, self.id)
        for row in self.curs.fetchall():
            tweet = Tweet(self.session, row)
            self.all_tweets.append(tweet)

        self.more_tweets()

    def more_tweets(self): 
        self.tweets = self.all_tweets[self.index - 3:self.index]
        self.more_exist = len(self.all_tweets) - self.index > 0
        self.index += 3

    def display(self, index=None):
        if index is not None:
            user_index = "Result %d" % (index + 1)
        else:
            user_index = "Result %d" % (self.id)

        col1_width = len(user_index) + 1
        col2_width = BORDER_LEN - col1_width - 3
        user_str = "%d (%s)" % (self.id, self.name)

        city_str = "%s" % (self.city)
        blank = " " * col1_width

        line1_1 = "{:{width}}".format(user_index, width=col1_width)
        line1_2 = " {:{width}}".format(user_str, width=col2_width)
        line2_2 = " {:{width}}".format(city_str, width=col2_width)
        line3_2 = " {:{width}}".format(self.email, width=col2_width)

        print_string(line1_1 + line1_2)
        print_string(blank + line2_2)

    def display_stats(self):
        print_newline()
        print_border(thick=True)
        print_string("User Statistics".upper())
        print_border(thick=True, sign='|')

        print_string("Username: %d" % (self.id))
        print_string("Name: %s" % (self.name))
        print_string("City: %s UTC (%s)" % (self.city, self.tz_str))
        print_string("Email: %s" % (self.email))
        print_string("Following: %d" % (self.following))
        print_string("Followers: %d" % (self.followers))
        print_string("Number of tweets: %d" % (self.num_tweets))
 
        print_newline(no_border=False)
        print_string("RECENT TWEETS")

        if len(self.tweets) == 0:
            print_string("%s does not have any tweets yet." % (self.name))
        else:
            for tweet in self.tweets:
                self.display_tweet(tweet) 

        return self.user_menu()

    def display_tweet(self, tweet):
        text1, text2 = tweet.split_text(tweet.get_text(), max_width=77)
        
        print_border(thick=False, sign='|')
        print_string(text1)
        if len(text2) > 1: 
            print_string(text2)
        print_string(tweet.tdate())

    def follow(self):
        if not follows_exists(self.curs, self.logged_user, self.id):
            prompt = "Are you sure you want to follow %s? y/n: " % (self.name)
            confirm = validate_yn(prompt, self.session)

            if confirm in ['y', 'yes']:
                insert_follow(self.conn, [self.logged_user, self.id, TODAY])
                print("You are now following %s." % (self.name))
                press_enter(self.session)
            else:
                self.display_stats()
        else:
            print("You are already following this user.")
            press_enter(self.session)
            self.display_stats()


class UserSearch:

    def __init__(self, session, keywords='', followers=False):
        self.session = session
        self.conn = session.get_conn()
        self.curs = session.get_curs() 
        self.user = session.get_username()
        self.all_results = []
        self.all_users = []
        self.users = []
        self.index = 5
        self.more_exist = False
        self.searched = keywords
        self.keywords = convert_keywords(keywords)
        self.category = "UserSearch"

    def get_category(self):
        return self.category

    def get_searched(self):
        width = 50
        if len(self.searched) > width:
            return self.searched[:width] + "..."
        else:
            return self.searched

    def get_follows(self):
        get_followers(self.curs, self.user)
        for row in self.curs.fetchall():
            self.all_results.append(row)

        self.add_results()
        self.more_results()

    def get_results(self):
        match_name(self.curs, self.keywords)
        for row in self.curs.fetchall():
            self.all_results.append(row)

        match_city(self.curs, self.keywords)
        for row in self.curs.fetchall():
            self.all_results.append(row)

        self.add_results()
        self.more_results()

    def add_results(self):
        for row in self.all_results:
            user = User(self.session, row)
            self.all_users.append(user) 

    def more_results(self):
        self.users = self.all_users[self.index - 5:self.index]
        self.more_exist = len(self.all_results) - self.index > 0
        self.index += 5 

    def display_results(self):
        print_border(thick=True) 
        title = "SEARCH RESULTS FOR %s" % (self.get_searched().upper())
        print_string(title)
        print_border(thick=True, sign='|') 

        for i, user in enumerate(self.users):
            user.display(index=i)

            if i == len(self.users) - 1:
                print_border(thick=False, sign='+')
            else:
                print_border(thick=False, sign='|')

        if len(self.users) == 0:
            print_string("Sorry, there are no users that match that query.")

    def select_result(self, user):
        choice = 0
        while choice < 3:
            choices = user.display_stats()
            choice = validate_num(SELECT, self.session, self.session.home, size=len(choices))
            option = choices[choice - 1]

            if option == "Follow": 
                user.follow()
            elif option == "See more tweets": 
                user.more_tweets()
                user.display_stats() 

        if option == "Go back": 
            self.session.home(self)
        elif option == "Do another search": 
            new_search = search_users(self.session)
            self.session.home(new_search)
        elif option == "Home": 
            self.session.home()
        elif option == "Logout": 
            self.session.logout()

    def choose_result(self):
        prompt = "Enter the result number to select: "
        choice = validate_num(prompt, self.session, size=len(self.users))
        if check_quit(choice):
            self.session.home(self)
        else:
            choice -= 1
 
        user = self.users[choice]
        self.select_result(user)

    def results_exist(self):
        return True if len(self.users) > 0 else False

    def more_results_exist(self):
        return self.more_exist 

