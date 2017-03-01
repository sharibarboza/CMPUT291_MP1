# Query helper methods

# ---------------------------- INSERT QUERIES ----------------------------------
def insert_user(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of usr, pwd, name, email, city, timezone values
	"""
    cursInsert = conn.cursor()
    cursInsert.execute("INSERT INTO users(usr,pwd,name,email,city,timezone)"
    	"VALUES(:1,:2,:3,:4,:5,:6)", data_list)
    conn.commit()

    return cursInsert

def insert_follow(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of flwer, flwee, start_date values
	"""
    cursInsert = conn.cursor()
    cursInsert.execute("INSERT INTO follows(flwer,flwee,start_date)"
    	"VALUES(:1,:2,:3)", data_list)
    conn.commit()

    return cursInsert

def insert_tweet(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of tid, writer, tdate, text, replyto values
	"""
	cursInsert = conn.cursor()
	cursInsert.execute("INSERT INTO tweets(tid,writer,tdate,text,replyto)"
		"VALUES(:1,:2,:3,:4,:5)", data_list)
	conn.commit()

	return cursInsert

def insert_hashtag(conn, term):
	"""
	param conn: connection (not cursor object)
	param term: single string containing a hashtag term
	"""
	cursInsert = conn.cursor()
	cursInsert.execute("INSERT INTO hashtags(term) VALUES(:1)", [term])
	conn.commit()

	return cursInsert

def insert_mention(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of tid, term values
	"""
	cursInsert = conn.cursor()
	cursInsert.execute("INSERT INTO mentions(tid,term)"
		"VALUES(:1,:2)", data_list)
	conn.commit()

	return cursInsert

def insert_retweet(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of usr, tid, rdate values
	"""
	cursInsert = conn.cursor()
	cursInsert.execute("INSERT INTO retweets(usr,tid,rdate)"
		"VALUES(:1,:2,:3)", data_list)
	conn.commit()

	return cursInsert

def insert_list(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of lname, owner values
	"""
	cursInsert = conn.cursor()
	cursInsert.execute("INSERT INTO lists(lname,owner)"
		"VALUES(:1,:2)", data_list)
	conn.commit()

	return cursInsert

def insert_include(conn, data_list):
	"""
	param conn: connection (not cursor object)
	param data_list: list of lname, member values
	"""
	cursInsert = conn.cursor()
	cursInsert.execute("INSERT INTO includes(lname,member)"
		"VALUES(:1,:2)", data_list)
	conn.commit()

	return cursInsert

# -------------------------- SPECIFIC SELECT QUERIES --------------------------------

def get_user(curs, username, password):
	"""
	Returns the tuple of a specific user from the database
	param curs: cursor object
	param username: user id (must be a number)
	param password: user password (4 char)
	"""
	curs.execute('SELECT * FROM users WHERE usr=:1 AND pwd=:2', [username,password])
	return curs.fetchone()

def user_exists(curs, user):
	"""
	Checks if a user exists in the database
	param curs: cursor object
	param user: user id (must be a number)
	"""
	curs.execute('SELECT usr FROM users WHERE usr=:1', [user])
	return curs.fetchone() is not None 



