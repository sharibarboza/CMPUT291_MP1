from constants import SELECT, TODAY

from utils import (
    convert_date, 
    display_selections, 
    validate_num,
    validate_yn,
)

from queries import (
    get_name,
    select,
    follows_tweets,
    get_rep_cnt,
    get_ret_cnt,
    get_user_from_tid,
    get_text_from_tid,
    already_retweeted,
    insert_retweet,
    insert_tweet,
    insert_mention,
    insert_hashtag,
    tid_exists,
    hashtag_exists,
)

def compose_tweet(conn, user, replyto=None):
    """
    Generates a new tweet and inserts it into the database
    """
    text = input("Enter tweet: ")
    writer = user
    tid = generate_tid(conn)
    date = TODAY
    replyto = replyto
    rt_user = None
    data = [tid, writer, date, text, replyto, rt_user]
    new_tweet = Tweet(conn, user, data)
    new_tweet.display()

    confirm = validate_yn("Confirm tweet? y/n: ")
    if confirm in ["n", "no"]:
        print("Tweet cancelled.")
        return
    else:
        insert_tweet(conn, new_tweet.get_values())
        print("Tweet %d created." % (new_tweet.id))

    new_tweet.set_terms()


def generate_tid(conn):
    """
    Generates a new unique tweet id
    """
    curs = conn.cursor()
    select(curs, 'tweets')
    new_tid = len(curs.fetchall()) + 1
    
    while tid_exists(curs, new_tid): 
        new_tid += 1
    curs.close()

    return new_tid


class Tweet:

    def __init__(self, conn, user, data):
        """
        Represents a single tweet, helps to display tweets to console
        param conn: database connection
        param user: logged in user (not the tweet writer)
        param data: row values from tweets table plus other values
        """
        self.conn = conn
        self.curs = conn.cursor()
        self.user = user

        self.id = data[0]
        self.writer = data[1]
        self.date = data[2]
        self.text = data[3]
        self.replyto = data[4]

        if self.replyto:
            self.reply_user = get_user_from_tid(self.curs, self.replyto)
            self.reply_name = get_name(self.curs, self.reply_user)
            self.reply_text = get_text_from_tid(self.curs, self.replyto)

        self.date_str = convert_date(self.date)
        self.rep_cnt = get_rep_cnt(self.curs, self.id)
        self.ret_cnt = get_ret_cnt(self.curs, self.id)
        self.writer_name = get_name(self.curs, self.writer)

    def display(self, user=None):
        """
        Displays basic info on a tweet
        Used for first screen after login or a tweet search
        """
        if user:
            user_name = get_name(self.curs, user)
            print("%s Retweeted" % (user_name))

        print("%s @%d - %s" % (self.writer_name, self.writer, self.date_str))
        print("%s\n" % (self.text))

    def display_stats(self):
        """
        Displays statistics on a tweet after a tweet has been selected
        """
        print("\nTWEET STATISTICS\n")
        print("Tweet ID: %d" % (self.id))
        print("Written by: %s @%d" % (self.writer_name, self.writer))
        print("Posted: %s" % (self.date_str))
        print("Text: %s" % (self.text))

        if (self.replyto):
            print("Reply to: %s (%s @%d)" % (self.reply_text, self.reply_name, self.reply_user))
        else:
            print("Reply to: None")

        print("Number of replies: %s" % (self.rep_cnt))
        print("Number of retweets: %s" % (self.ret_cnt))

    def tweet_menu(self):
        """
        Displays options to reply or retweet a tweet after it has 
        been selected
        """
        choices = ["Reply", "Retweet", "Home", "Logout"]
        display_selections(choices)
        choice = validate_num(SELECT, size=len(choices))

        if choice == 1:
            compose_tweet(self.conn, self.user)
        elif choice == 2:
            self.retweet()
        return choice

    def retweet(self):
        """
        Allows logged in user to retweet a selected tweet and 
        insert retweet into the database
        """
        if already_retweeted(self.curs, self.user, self.id):
            print("You already retweeted this tweet.")
            return
            
        self.display(self.user)
        confirm = validate_yn("Confirm retweet? y/n: ")
        if confirm in ["n", "no"]:
            print("Retweet cancelled.")
        else:
            print("Retweeted - %s" % (TODAY))
            data_list = [self.user, self.id, TODAY]
            insert_retweet(self.conn, data_list)

    def get_values(self):
        """
        Returns a list of tid, writer, tdate, text, and replyto
        """
        return [self.id, self.writer, self.date, self.text, self.replyto]

    def set_terms(self):
        """
        Finds the hashtags in a tweet and insert them into the
        hashtags and mentions tables
        """
        hashtags = self.find_hashtags()
        for tag in hashtags:
            term = self.extract_term(tag)
           
            if not hashtag_exists(self.curs, term):
                insert_hashtag(self.conn, term)     
            insert_mention(self.conn, [self.id, term])

    def extract_term(self, index):
        """
        Get the hashtag term in the tweet based on the index
        """
        space_index = self.text.find(' ', index)
        if space_index < 0:
            space_index = len(self.text) + 1

        return self.text[index + 1:space_index]

    def find_hashtags(self):
        """
        Returns a list of all indexes of found hashtags
        """
        index_list = []
        for i, ch in enumerate(self.text):
            if ch == '#':
                index_list.append(i)
        return index_list

class TweetSearch:

    def __init__(self, conn, user):
        """
        Can be used for getting tweets of users being followed or 
        searching for specific tweets based on keywords
        param conn: database connection
        param user: logged in user id
        """ 
        self.conn = conn 
        self.user = user
        self.tweets = []

    def get_user_tweets(self):
        """
        Find tweets/retweets from users are being followed
        """
        curs = self.conn.cursor()
        follows_tweets(curs, self.user)

        self.rows = curs.fetchmany(5)
        self.display_tweets()
       
        if len(self.rows) > 0:
            return curs
        else:
            curs.close()
            return None 

    def display_tweets(self):
        """
        Display resulting tweets 5 at a time ordered by date
        """
        for i, row in enumerate(self.rows, 1):
            print("Tweet %d" % (i))
            tweet = Tweet(self.conn, self.user, data=row)
            self.tweets.append(tweet)
   
            rt_user = row[5]
            if tweet.writer != rt_user: 
                tweet.display(rt_user)
            else:
                tweet.display() 

        if len(self.rows) == 0:
            print("You have no tweets yet.")

    def select_tweet(self):
        """
        Prompt user to choose one of the displayed tweets
        """
        tweet_num = self.choose_tweet()
        tweet = self.tweets[tweet_num - 1]
        tweet.display_stats()

        choice = 0
        while choice < 3:
            choice = tweet.tweet_menu()

        if choice == 4:
            choice = 6
        return choice 

    def choose_tweet(self):
        """
        Get the number of the tweet the user wants to select
        """
        choices = []
        for i, row in enumerate(self.rows, 1):
            tweet_str = "Tweet %d" % (i)
            choices.append(tweet_str)

        display_selections(choices)
        return validate_num(SELECT, size=len(choices))

