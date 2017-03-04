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

def find_user(curs, username, password):
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
    Gets a specific user
    """
    curs.execute('select name from users where usr=:1', [user])
    return curs.fetchone()[0].rstrip()

def get_user_from_tid(curs, tid):
    """
    Gets the name of the writer of a specified tweet
    """
    curs.execute('select usr from users, tweets where tid=:1 '
        'and writer = usr', [tid])
    return curs.fetchone()[0]

def get_text_from_tid(curs, tid):
    """
    Gets the text from the specified tweet
    """
    curs.execute('select text from tweets where tid=:1', [tid])
    return curs.fetchone()[0].rstrip()

def create_tStat(curs):
    """
    Create view tStat to return statistics about a tweet including
    tid, writer, tdate, text, retweet count, reply count, and 
    mention count
    """
    curs.execute('drop view tStat')
    curs.execute('create view tStat (tid, writer, tdate, text, rep_cnt, '
        'ret_cnt, sim_cnt) as select t.tid, t.writer, t.tdate, t.text, '
        'count(distinct t2.tid), count(distinct rt.usr), count(distinct m2.tid) '
        'from (((tweets t left outer join tweets t2 on t.writer = t2.replyto) '
        'left outer join retweets rt on t.tid = rt.tid) '
        'left outer join mentions m on t.tid = m.tid) '
        'left outer join mentions m2 on m.term = m2.term '
        'group by t.tid, t.writer, t.tdate, t.text')

def get_rep_cnt(curs, tid):
    """
    Get the reply count of a specific tweet
    param: tid - tweet id
    """
    curs.execute('select rep_cnt from tStat where tid=:1', [tid])
    return curs.fetchone()

def get_ret_cnt(curs, tid):
    """
    Get the retweetn count of a specific tweet
    param: tid - tweet id
    """
    curs.execute('select ret_cnt from tStat where tid=:1', [tid])
    return curs.fetchone()

def already_retweeted(curs, user, tid):
    """
    Returns true if the user has already tweeted the specific tweet
    """
    curs.execute('select * from retweets where usr=:1 and tid=:2', [user, tid])
    return False if curs.fetchone() is None else True
