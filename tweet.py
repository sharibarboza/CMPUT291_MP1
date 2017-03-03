from utils import (
    convert_date, 
    display_selections,
    validate_num,
    add_main_menu
)

from queries import follows_tweets, get_name
from constants import BORDER, SELECT

class TweetSearch:

    def __init__(self, conn, user=None):
        self.conn = conn
        self.user = user

        if user:
            self.get_user_tweets()

    def get_user_tweets(self):
        curs = self.conn.cursor()
        follows_tweets(curs, self.user)

        rows = curs.fetchmany(5)
        self.display_tweets(rows)
        self.get_option(curs)

    def display_tweets(self, rows):
        for i, row in enumerate(rows, 1):
            t_writer = row[1]
            t_date = convert_date(row[2])
            t_text = row[3]
            t_replyto = row[4]
            t_rt = row[5]

            nameCurs = self.conn.cursor()
            writer_name = get_name(nameCurs, t_writer)

            print("Tweet %d" % (i))

            # Indicate retweet
            if t_writer != t_rt:
                rt_name = get_name(nameCurs, t_rt)
                print("%s Retweeted" % (rt_name))

            print("%s @%d - %s" % (writer_name, t_writer, t_date))
            print("%s\n" % (t_text))

    def get_option(self, curs):
        rows = curs.fetchmany(5)
        choices = ["Select tweet"]

        if (len(rows) > 0):
            choices.insert(1, "See more tweets")

        add_main_menu(choices)
        display_selections(choices)
        choice = validate_num(SELECT, size=len(choices))






