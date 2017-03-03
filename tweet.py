from utils import (
    convert_date, 
    display_selections,
    validate_num,
)

from constants import SELECT
from queries import follows_tweets, get_name

class Tweet:

    def __init__(self, row):
        self.__writer = row[1]
        self.__date = row[2]
        self.__text = row[3]
        self.__replyto = row[4]
        self.__rt = row[5]
        self.__date_str = convert_date(self.__date)

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
            return None 

    def display_tweets(self):
        nameCurs = None
        for i, row in enumerate(self.rows, 1):
            tweet = Tweet(row)
            self.tweets.append(tweet)

            nameCurs = self.conn.cursor()
            writer_name = get_name(nameCurs, tweet.writer)

            print("Tweet %d" % (i))

            # Indicate retweet
            if  tweet.is_retweet():
                rt_name = get_name(nameCurs, tweet.rt)
                print("%s Retweeted" % (rt_name))

            print("%s @%d - %s" % (writer_name, tweet.writer, tweet.date_str))
            print("%s\n" % (tweet.text))

        if len(self.rows) == 0:
            print("You have no tweets yet.")
        nameCurs.close()

    def select_tweet(self):
        tweet_num = self.choose_tweet()
        tweet = self.tweets[tweet_num]
        self.display_tweet_stats(tweet)

    def choose_tweet(self):
        choices = []
        for i, row in enumerate(self.rows, 1):
            tweet_str = "Tweet %d" % (i)
            choices.append(tweet_str)

        display_selections(choices)
        return validate_num(SELECT, size=len(choices))

    def display_tweet_stats(self, tweet):
        print(tweet.text)



