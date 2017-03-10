from utils import is_hashtag, remove_hashtags

# Query helper methods

# ---------------------------- INSERT QUERIES ----------------------------------
def insert_user(conn, data_list):
    """ Inserts new user into users table

    :param conn: connection (not cursor object)
    :param data_list: list of usr, pwd, name, email, city, timezone values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into users(usr,pwd,name,email,city,timezone)"
    	"values(:1,:2,:3,:4,:5,:6)", data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_follow(conn, data_list):
    """ Inserts new follow relationship into follows table

    :param conn: connection (not cursor object)
    :param data_list: list of flwer, flwee, start_date values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into follows(flwer,flwee,start_date)"
    	"values(:1,:2,:3)", data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_tweet(conn, data_list):
    """ Inserts new tweet into tweets table

    :param conn: connection (not cursor object)
    :param data_list: list of tid, writer, tdate, text, replyto values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into tweets(tid,writer,tdate,text,replyto)"
	    "values(:1,:2,:3,:4,:5)", data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_hashtag(conn, term):
    """ Inserts new hashtag into hashtags table

    :param conn: connection (not cursor object)
    :param term: single string containing a hashtag term
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into hashtags(term) values(:1)", [term.lower()])
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_mention(conn, data_list):
    """ Inserts new mention into mentions table

    :param conn: connection (not cursor object)
    :param data_list: list of tid, term values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into mentions(tid,term) values(:1,:2)",
        data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_retweet(conn, data_list):
    """ Inserts new retweet into retweets table

    :param conn: connection (not cursor object)
    :param data_list: list of usr, tid, rdate values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into retweets(usr,tid,rdate) values(:1,:2,:3)", 
        data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_list(conn, data_list):
    """ Inserts new list into lists table

    :param conn: connection (not cursor object)
    :param data_list: list of lname, owner values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into lists(lname,owner) values(:1,:2)",
        data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

def insert_include(conn, data_list):
    """ Inserts new include into includes table

    :param conn: connection (not cursor object)
    :param data_list: list of lname, member values
    """
    cursInsert = conn.cursor()
    cursInsert.execute("insert into includes(lname,member) values(:1,:2)",
        data_list)
    cursInsert.close()
    conn.commit()

    return cursInsert

# -------------------------- SPECIFIC SELECT QUERIES --------------------------------

def find_user(curs, username, password):
    """ Returns the tuple of a specific user from the database
    
    :param curs: cursor object
    :param username: user id (must be a number)
    :param password: user password (4 char)
    """
    curs.execute('select * from users where usr=:1 and pwd=:2', [username,password])
    return curs.fetchone()

def user_exists(curs, user):
    """ Checks if a user exists in the database
    
    :param curs: cursor object
    :param user: user id (must be a number)
    """
    curs.execute("select usr from users where usr like '%%' || :1 || '%%'", [user])
    return curs.fetchone() is not None 

def follows_exists(curs, flwer, flwee):
    """ Checks if a follows relationship exists in the database

    :param curs: cursor object
    :param flwer: follower user id
    :param flwee: followee user id
    """
    curs.execute('select * from follows where flwer=:1 and flwee=:2', [flwer, flwee])
    return curs.fetchone() is not None

def tid_exists(curs, tid):
    """ Checks if a tweet id exists in the database
    
    :param curs: cursor object
    :param tid: tweet id
    """
    curs.execute('select tid from tweets where tid=:1', [tid])
    return curs.fetchone() is not None

def hashtag_exists(curs, term):
    """ Checks if a hashtag term exists in the database
    
    :param curs: cursor object
    :param term: hashtag word
    """
    curs.execute("select term from hashtags where term like '%%' || :1 || '%%'", [term])
    return curs.fetchone() is not None

def mention_exists(curs, tid, term):
    """ Checks if a mention exists in the database
    
    :param curs: cursor object
    :param tid: tweet id
    :param term: hashtag word
    """
    curs.execute("select term from mentions where tid=:1 and term like '%%' || :2 || '%%'",
        [tid, term])
    return curs.fetchone() is not None

def list_exists(curs, lname, owner):
    """ Checks if a list exists in the database
 
    :param curs: cursor object
    :param lname: list name
    :param owner: user id of list owner
    """
    curs.execute("select * from lists where lname like '%%' || :1 || '%%' " 
        "and owner=:2", [lname, owner])
    return curs.fetchone() is not None

def select(curs, table):
    """ Select rows from a table 
    
    :param curs: cursor object
    :param table: name of table to select from
    """
    curs.execute("select * from %s" % (table))

def follows_tweets(curs, user):
    """ Gets the tweets/retweets from users who are being followed by the user
    Ordered by tweet date
    
    :param curs: cursor boejct
    :param user: logged-in user id
    """
    curs.execute('select distinct t.tid, t.writer, t.tdate, t.text, t.replyto, t2.usr '
        'from tweets t left outer join (select f.flwer, f.flwee, rt.usr, rt.tid '
        'from follows f left outer join retweets rt on f.flwee = rt.usr) t2 '
        'on t.tid = t2.tid or (t.writer = t2.flwee) where t2.flwer =:1 order by t.tdate desc', 
        [user])

def get_followers(curs, user):
    """Gets all the followers of a specific user

    :param curs: cursor object
    :param user: user id
    """
    curs.execute("select u.usr, u.pwd, u.name, u.email, u.city, u.timezone from "
        "users u, follows f where u.usr = f.flwer and f.flwee=:1 "
        "order by f.start_date desc", [user])

def get_name(curs, user):
    """Gets a specific user's name
    
    :param curs: cursor object
    :param user: a user's id
    """
    curs.execute('select name from users where usr=:1', [user])
    return curs.fetchone()[0].rstrip()

def get_user_from_tid(curs, tid):
    """ Gets the name of the writer of a specified tweet
    
    :param curs: cursor object
    :param tid: a tweet's id
    """
    curs.execute('select usr from users, tweets where tid=:1 '
        'and writer = usr', [tid])
    return curs.fetchone()[0]

def get_text_from_tid(curs, tid):
    """ Gets the text from the specified tweet
    
    :param curs: cursor object
    :param tid: a tweet's id
    """
    curs.execute('select text from tweets where tid=:1', [tid])
    return curs.fetchone()[0].rstrip()

def create_tStat(curs):
    """ Create view tStat to return statistics about a tweet including
    tid, writer, tdate, text, retweet count, reply count, and 
    mention count

    :param curs: cursor object
    """
    curs.execute('create view tStat (tid, writer, tdate, text, rep_cnt, '
        'ret_cnt, sim_cnt) as select t.tid, t.writer, t.tdate, t.text, '
        'count(distinct t2.tid), count(distinct rt.usr), count(distinct m2.tid) '
        'from (((tweets t left outer join tweets t2 on t.writer = t2.replyto) '
        'left outer join retweets rt on t.tid = rt.tid) '
        'left outer join mentions m on t.tid = m.tid) '
        'left outer join mentions m2 on m.term = m2.term '
        'group by t.tid, t.writer, t.tdate, t.text')

def create_uStat(curs):
    """ Create view uStat to return statistics about a user including
    usr, follower count, followee count, tweet count, and 3 recent weets

    :param curs: cursor object
    """
    curs.execute('create view uStat (usr, flwer_cnt, flwee_cnt, tw_cnt) as '
        'select u.usr, t1.ee_cnt, t2.er_cnt, nvl(t3.tw_cnt, 0) '
        'from (((users u left outer join '
        '(select u1.usr, count(ee.flwee) as ee_cnt '
        'from (users u1 full outer join follows ee on ee.flwer = u1.usr) '
        'group by u1.usr) t1 on u.usr = t1.usr) '
        'left outer join '
        '(select u2.usr, count(er.flwee) as er_cnt '
        'from (users u2 full outer join follows er on er.flwee = u2.usr) '
        'group by u2.usr) t2 on t1.usr = t2.usr) '
        'left outer join '
        '(select tw1.writer, count(distinct tw1.tid) as tw_cnt '
        'from tweets tw1 group by tw1.writer) t3 on t3.writer = t1.usr) '
        'order by t1.usr')

def tStat_exists(curs):
    curs.execute("select view_name from user_views where view_name='TSTAT'")
    return curs.fetchone() is not None

def uStat_exists(curs):
    curs.execute("select view_name from user_views where view_name='USTAT'")
    return curs.fetchone() is not None

def get_user_stats(curs, user):
    """Get user statistics about a specific user"""
    curs.execute("select * from uStat where usr=:1", [user])
    return curs.fetchmany(3)

def get_user_tweets(curs, user):
    """Get all the tweets of a specific user

    :param user: user id
    """
    curs.execute('select * from tweets where writer=:1 order by tdate desc', [user])

def get_rep_cnt(curs, tid):
    """ Get the reply count of a specific tweet
    
    param curs: cursor object
    param: tid: a tweet's id
    """
    curs.execute('select rep_cnt from tStat where tid=:1', [tid])
    return curs.fetchone()

def get_ret_cnt(curs, tid):
    """ Get the retweetn count of a specific tweet
    
    param curs: cursor object
    param: tid: a tweet's id
    """
    curs.execute('select ret_cnt from tStat where tid=:1', [tid])
    return curs.fetchone()

def get_hashtags(curs, tid):
    """ Get all the hashtags for a tweet"""
    curs.execute('select term from mentions m where m.tid=:1', [tid])
    return [row[0].rstrip() for row in curs.fetchall()] 

def already_retweeted(curs, user, tid):
    """ Returns true if the user has already tweeted the specific tweet
    
    param curs: cursor object
    param user: a user's id
    param tid: a tweet's id
    """
    curs.execute('select * from retweets where usr=:1 and tid=:2', [user, tid])
    return False if curs.fetchone() is None else True

def match_tweet(curs, keywords, order):
    """Matches tweets who satisfy at least one keyword 

    :param curs: cursor object
    :param keywords: list of tokenized words
    :param order: what to order results by
    """
    if len(keywords) == 0:
        return

    q = "select distinct t.tid, t.writer, t.tdate, t.text, t.replyto from tweets t " \
        "full outer join mentions m on t.tid=m.tid where"
    term_q = " m.term like '%%' || :%d || '%%'"
    text_q = " lower(t.text) like '%%' || :%d || '%%'"
    
    if is_hashtag(keywords[0]):
        q += term_q % (1)
    else:
        q += text_q % (1)

    for i in range(2, len(keywords) + 1):
        if is_hashtag(keywords[i-1]):
            q += " or" + term_q % (i)
        else:
            q += " or" + text_q % (i)
    q += " order by %s desc" % (order)

    terms = remove_hashtags(keywords)
    curs.execute(q, terms)

def match_name(curs, keywords):
    """Matches users whose names contain the keyword

    :param curs: cursor object
    :param keywords: input string (e.g. 'John', 'John Doe') 
    """
    if len(keywords) == 0:
        return

    q = "select * from users where "
    name_q = " lower(name) like '%%' || :%d || '%%'"

    q += name_q % (1)

    for i in range(2, len(keywords) + 1):
        q += " or" + name_q % (i)
    q += " order by length(trim(name))"
    curs.execute(q, keywords)

def match_city(curs, keywords):
    """Matches users whose cities contain the keyword

    :param curs: cursor object
    :param keywords: input string (e.g. 'Edmonton', 'New York') 
    """
    if len(keywords) == 0:
        return

    temp = []
    for word in keywords:
        temp.append(word)
        temp.append(word)

    q = "select * from users where "
    name_q = " lower(city) like '%%' || :%d || '%%' and lower(name) not like '%%' || :%d || '%%'"

    q += name_q % (1, 2)

    for i in range(2, len(keywords) + 1):
        q += " or" + name_q % (i, i + 1)
    q += " order by length(trim(city))"
    curs.execute(q, temp)   

