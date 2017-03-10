from queries import *
from utils import *


def search_users(session):
    """Matches users/cities to keywords

    :param session: Session object
    """
    search_input = validate_str("Enter keyword for user search: ", session, session.home, null=False)
    s_users = UserSearch(session, search_input)
    s_users.get_results()
    return s_users


class User:

    def __init__(self, session, data):
        self.session = session
        self.conn = session.get_conn()
        self.curs = self.conn.cursor()
        self.logged_user = session.get_username()

        self.id = data[0]
        self.pwd = data[1]
        self.name = data[2].rstrip()
        self.email = data[3].rstrip()
        self.city = data[4].rstrip()
        self.timezone = data[5]
        self.tz_str = convert_timezone(self.timezone)

    def user_menu(self):
        choices = ["Follow", "See more tweets", "Select another user", "Home", "Logout"]
        print_border(thick=True)
        display_selections(choices)

        return choices

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

        print_string("User ID: %d" % (self.id))
        print_string("Name: %s" % (self.name))
        print_string("City: %s UTC (%s)" % (self.city, self.tz_str))
        print_string("Email: %s" % (self.email))
        return self.user_menu()

    def follow(self):
        if not follows_exists(self.curs, self.logged_user, self.id):
            prompt = "Are you sure you want to follow %s? y/n: " % (self.name)
            confirm = validate_yn(prompt, self.session)

            if confirm in ['y', 'yes']:
                insert_follow(self.conn, [self.logged_user, self.id, TODAY])
                print("You are now following %s." % (self.name))
                press_enter()
            else:
                self.display_stats()
        else:
            print("You are already following this user.")
            press_enter()
            self.display_stats()


class UserSearch:

    def __init__(self, session, keywords=''):
        self.session = session
        self.conn = session.get_conn()
        self.curs = self.conn.cursor()
        self.user = session.get_username()
        self.all_results = []
        self.all_users = []
        self.users = []
        self.index = 5
        self.more_exist = False
        self.searched = keywords
        self.keywords = convert_keywords(keywords)

    def get_searched(self):
        width = 50
        if len(self.searched) > width:
            return self.searched[:width] + "..."
        else:
            return self.searched

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
   
    def results_exist(self):
        return True if len(self.users) > 0 else False

    def more_results_exist(self):
        return self.more_exist 

    def select_result(self, user):
        choice = 0
        while choice < 3:
            choices = user.display_stats()
            choice = validate_num(SELECT, self.session, self.session.home, size=len(choices))

            if choice == 1:
                user.follow()
            elif choice == 2:
                user.get_tweets()                    
            elif choice == 3:
                self.display_results()
                self.choose_result()

        if choice == 5:
            self.session.logout()

    def choose_result(self):
        prompt = "Enter the result number to select: "
        choice = validate_num(prompt, self.session, self.session.home, size=len(self.users)) - 1

        user = self.users[choice]
        self.select_result(user)

