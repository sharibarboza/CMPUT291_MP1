from queries import *
from utisl import *

class UserSearch:

    def __init__(self, session):
        self.session = session
        self.conn = session.get_conn()
        self.curs = self.conn.cursor()
        self.user = self.get_username()
