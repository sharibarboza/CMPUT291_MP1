# Query helper methods

# ---------------------------- INSERT QUERIES ----------------------------------
def insert_user(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of usr, pwd, name, email, city, timezone values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into users(usr,pwd,name,email,city,timezone)"
    	"values(:1,:2,:3,:4,:5,:6)", data_list)
    conn.commit()

    return cursInsert

def insert_follow(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of flwer, flwee, start_date values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into follows(flwer,flwee,start_date)"
    	"values(:1,:2,:3)", data_list)
    conn.commit()

    return cursInsert

def insert_tweet(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of tid, writer, tdate, text, replyto values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into tweets(tid,writer,tdate,text,replyto)"
	    "values(:1,:2,:3,:4,:5)", data_list)
    conn.commit()

    return cursInsert

def insert_hashtag(conn, term):
    """
    param conn: connection (not cursor object)
    param term: single string containing a hashtag term
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into hashtags(term) values(:1)", [term])
    conn.commit()

    return cursInsert

def insert_mention(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of tid, term values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into mentions(tid,term)"
	    "values(:1,:2)", data_list)
    conn.commit()

    return cursInsert

def insert_retweet(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of usr, tid, rdate values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into retweets(usr,tid,rdate)"
	    "values(:1,:2,:3)", data_list)
    conn.commit()

    return cursInsert

def insert_list(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of lname, owner values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into lists(lname,owner)"
	    "values(:1,:2)", data_list)
    conn.commit()

    return cursInsert

def insert_include(conn, data_list):
    """
    param conn: connection (not cursor object)
    param data_list: list of lname, member values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into includes(lname,member)"
	    "values(:1,:2)", data_list)
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
    curs.execute('select * from users where usr=:1 and pwd=:2', [username,password])
    return curs.fetchone()

def user_exists(curs, user):
    """
    Checks if a user exists in the database
    param curs: cursor object
    param user: user id (must be a number)
    """
    curs.execute('select usr from users where usr=:1', [user])
    return curs.fetchone() is not None 

def select(curs, table):
    """
    Select rows from a table 
    """
    curs.execute("select * from %s" % (table))

def follows_tweets(curs, user):
    """
    Gets the tweets/retweets from users who are being followed by the user
    Ordered by tweet date
    param user: logged-in user
    """
    curs.execute('select distinct t.tid, t.writer, t.tdate, t.text, t.replyto, t2.usr '
        'from tweets t left outer join (select f.flwer, f.flwee, rt.usr, rt.tid '
        'from follows f left outer join retweets rt on f.flwee = rt.usr) t2 '
        'on t.tid = t2.tid or (t.writer = t2.flwee) where t2.flwer =:1 order by t.tdate desc', 
        [user])

def get_name(curs, user):
    """
    Gets the name of the specified user
    """
    curs.execute('select name from users where usr=:1', [user])
    return curs.fetchone()[0].rstrip()