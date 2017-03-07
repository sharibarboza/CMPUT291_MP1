from constants import SELECT, TODAY, BORDER, BORDER_LEN
from utils import *
from queries import * 


class UserSearch:

	def __init__(self, session, user, keywords=''):
		self.session = session
		self.user = user
		self.keywords = convert_keywords(keywords)