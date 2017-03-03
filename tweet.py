from utils import convert_date, display_selections, validate_num
from constants import SELECT

from queries import (
    follows_tweets,
    get_name,
    get_user_from_tid,
    get_text_from_tid,
    get_rep_cnt,
    get_ret_cnt
)

class Tweet:

    def __init__(self, row, conn):
        self.curs = conn.cursor()
        self.id = row[0]
        self.writer = row[1]
        self.writer_name = get_name(self.curs, self.writer)
        self.date = row[2]
        self.text = row[3]
        self.replyto = row[4]
        self.rt = row[5]
        
        self.date_str = convert_date(self.date)
        self.rep_cnt = get_rep_cnt(self.curs, self.id)
        self.ret_cnt = get_ret_cnt(self.curs, self.id)

        if self.replyto:
            self.reply_usr = get_user_from_tid(self.curs, self.replyto)
            self.reply_name = get_name(self.curs, self.reply_usr)
            self.reply_text = get_text_from_tid(self.curs, self.replyto)

        if self.rt:
            self.rt_name = get_name(self.curs, self.rt)

    def display(self, i):
        print("Tweet %d" % (i))

        # Indicate retweet
        if self.is_retweet():
            print("%s Retweeted" % (self.rt_name))

        print("%s @%d - %s" % (self.writer_name, self.writer, self.date_str))
        print("%s\n" % (self.text))

    def display_stats(self):
        print("\nTweet Statistics\n")
        print("Tweet id: %d" % (self.id))
        print("Written by: %s @%d" % (self.writer_name, self.writer))
        print("Posted: %s" % (self.date_str))
        print("Text: %s" % (self.text))

        if (self.replyto):
            print("Reply to: %s (%s @%d)" % (self.reply_text, self.reply_name, self.reply_usr))
        else:
            print("Reply to: None")

        print("Number of replies: %s" % (self.rep_cnt))
        print("Number of retweets: %s" % (self.ret_cnt))


    def is_retweet(self):
        return self.writer != self.rt


class TweetSearch:

    def __init__(self, conn, user=None):
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
            tweet = Tweet(row, self.conn)
            self.tweets.append(tweet)

            tweet.display(i)

        if len(self.rows) == 0:
            print("You have no tweets yet.")

    def select_tweet(self):
        tweet_num = self.choose_tweet()
        tweet = self.tweets[tweet_num - 1]
        tweet.display_stats()

    def choose_tweet(self):
        choices = []
        for i, row in enumerate(self.rows, 1):
            tweet_str = "Tweet %d" % (i)
            choices.append(tweet_str)

        display_selections(choices)
        return validate_num(SELECT, size=len(choices))




