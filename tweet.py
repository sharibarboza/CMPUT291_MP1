from utils import (
    convert_date, 
    display_selections,
    validate_num,
)

from constants import SELECT
from queries import follows_tweets, get_name

class Tweet:

    def __init__(self, row, conn):
        self.__id = row[0]
        self.__writer = row[1]
        self.__date = row[2]
        self.__text = row[3]
        self.__replyto = row[4]
        self.__rt = row[5]
        self.__date_str = convert_date(self.__date)

        nameCurs = conn.cursor()
        self.__writer_name = get_name(nameCurs, self.__writer)
        self.__rt_name = get_name(nameCurs, self.__rt)
        nameCurs.close()

    @property
    def writer(self):
        return self.__writer

    @property
    def date(self):
        return self.__date

    @property
    def text(self):
        return self.__text

    @property
    def replyto(self):
        return self.__replyto

    @property
    def rt(self):
        return self.__rt

    @property
    def date_str(self):
        return self.__date_str

    def display(self, i):
        print("Tweet %d" % (i))

        # Indicate retweet
        if self.is_retweet():
            print("%s Retweeted" % (self.__rt_name))

        print("%s @%d - %s" % (self.__writer_name, self.__writer, self.__date_str))
        print("%s\n" % (self.__text))

    def display_stats(self):
        print("\nTweet Statistics\n")
        print("Tweet id: %d" % (self.__id))
        print("Written by: %s @%d" % (self.__writer_name, self.__writer))
        print("Posted: %s" % (self.__date_str))
        print("Text: %s" % (self.__text))

        if (self.__replyto):
            print("Reply to: %s @%d" % (self.__rt_name, self.__rt))
        else:
            print("Reply to: None")

    def is_retweet(self):
        return self.__writer != self.__rt


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




