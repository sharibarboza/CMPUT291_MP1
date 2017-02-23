import sys
import cx_Oracle


"""
Usage Example:
from connect import Connect

curs = Connect('sql_login.txt').get_connection()

curs.close_conections()
"""

class Connect():

	connStr = "%s/%s@gwynne.cs.ualberta.ca:1521:CRS"

	def __init__(self, filename):

		file = open(filename)
		self.username = file.readline()
		self.password = file.readline()
		file.close()
		self.curs = None

		try:
			self.connection = cx_Oracle.connect(connStr % (self.username, self.password))
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print(sys.stderr, "Oracle code:", error.code)
			print(sys.stderr, "Oracle message:", error.message)

	def get_connection(self):
		return self.connection

	def close_connections(self):
		self.curs.close()
		self.connection.close()