from queries import *
from utils import *


def search_users(session):
    """Matches users/cities to keywords

    :param session: Session object
    """
    search_input = validate_str("Enter keyword: ", session, session.home)
    s_users = UserSearch(session, search_input)
    s_users.get_users()
    return s_users


class UserSearch:

    def __init__(self, session, keywords=''):
        self.session = session
        self.conn = session.get_conn()
        self.curs = self.conn.cursor()
        self.user = session.get_username()
        self.all_results = []
        self.users = []
        self.index = 5
        self.more_exist = False
        self.searched = keywords
        self.keywords = convert_keywords(keywords)

    def category(self):
        return "SearchUser"
 
    def get_searched(self):
        width = 50
        if len(self.searched) > width:
            return self.searched[:width] + "..."
        else:
            return self.searched

    def get_users(self):
        match_name(self.curs, self.keywords)
        for row in self.curs.fetchall():
            self.all_results.append(row)

        match_city(self.curs, self.keywords)
        for row in self.curs.fetchall():
            self.all_results.append(row)

        self.more_users()

    def more_users(self):
        self.users = self.all_results[self.index - 5:self.index]
        self.more_exist = len(self.all_results) - self.index > 0
        self.index += 5 

    def display_results(self):
        for row in self.all_results:
            print(row)
   
    def results_exist(self):
        return True if len(self.users) > 0 else False

    def more_results_exist(self):
        return self.more_exist 
