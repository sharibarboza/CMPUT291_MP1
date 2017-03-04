from constants import SELECT, TODAY

from utils import (
    convert_date, 
    display_selections, 
    validate_num,
    validate_yn
)

from queries import (
    follows_tweets,
    get_name,
    get_user_from_tid,
    get_text_from_tid,
    get_rep_cnt,
    get_ret_cnt,
    insert_retweet,
    already_retweeted
)

class Tweet:

    def __init__(self, row, conn):
        self.conn = conn
        self.curs = conn.cursor()
        self.id = row[0]
        self.writer = row[1]
        self.writer_name = get_name(self.curs, self.writer)
        self.date = row[2]
        self.text = row[3]
        self.replyto = row[4]
        self.rt_user = row[5]

        self.date_str = convert_date(self.date)
        self.rep_cnt = get_rep_cnt(self.curs, self.id)
        self.ret_cnt = get_ret_cnt(self.curs, self.id)

        if self.replyto:
            self.reply_user = get_user_from_tid(self.curs, self.replyto)
            self.reply_name = get_name(self.curs, self.reply_user)
            self.reply_text = get_text_from_tid(self.curs, self.replyto)

        if self.rt_user:
            self.rt_name = get_name(self.curs, self.rt_user)

    def display(self, user=None):
        if self.is_retweet(): 
            print("%s Retweeted" % (self.rt_name))         
        elif user:
            user_name = get_name(self.curs, user)
            print("%s Retweeted" % (user_name))

        print("%s @%d - %s" % (self.writer_name, self.writer, self.date_str))
        print("%s\n" % (self.text))

    def display_stats(self):
        print("\nTWEET STATISTICS\n")
        print("Tweet id: %d" % (self.id))
        print("Written by: %s @%d" % (self.writer_name, self.writer))
        print("Posted: %s" % (self.date_str))
        print("Text: %s" % (self.text))

        if (self.replyto):
            print("Reply to: %s (%s @%d)" % (self.reply_text, self.reply_name, self.reply_user))
        else:
            print("Reply to: None")

        print("Number of replies: %s" % (self.rep_cnt))
        print("Number of retweets: %s" % (self.ret_cnt))

    def tweet_menu(self, user):
        choices = ["Reply", "Retweet", "Home"]
        display_selections(choices)
        choice = validate_num(SELECT, size=len(choices))

        if choice == 2:
            self.retweet(user)

    def retweet(self, user):
        if not already_retweeted(self.curs, user, self.id):
            self.display(user)
            choice = validate_yn("Confirm retweet? y/n: ")
            if choice in ["n", "no"]:
                print("Retweet cancelled.")
            else:
                print("Retweeted - %s" % (TODAY))
                data_list = [user, self.id, TODAY]
                insert_retweet(self.conn, data_list)
        else:
            print("You already retweeted this tweet.")

    def is_retweet(self):
        return self.writer != self.rt_user


class TweetSearch:

    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        self.tweets = []

    def get_user_tweets(self):
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
        for i, row in enumerate(self.rows, 1):
            print("Tweet %d" % (i))
            tweet = Tweet(row, self.conn)
            self.tweets.append(tweet)
            tweet.display()

        if len(self.rows) == 0:
            print("You have no tweets yet.")

    def select_tweet(self):
        tweet_num = self.choose_tweet()
        tweet = self.tweets[tweet_num - 1]
        tweet.display_stats()
        tweet.tweet_menu(self.user)

    def choose_tweet(self):
        choices = []
        for i, row in enumerate(self.rows, 1):
            tweet_str = "Tweet %d" % (i)
            choices.append(tweet_str)

        display_selections(choices)
        return validate_num(SELECT, size=len(choices))




