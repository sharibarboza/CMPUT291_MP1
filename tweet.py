from utils import convert_date
from queries import follows_tweets, get_name
from constants import BORDER

class TweetSearch:

    def __init__(self, conn, user=None):
        self.conn = conn
        self.user = user

        if user:
            self.get_user_tweets()

    def get_user_tweets(self):
        curs = self.conn.cursor()
        follows_tweets(curs, self.user)
        self.display_tweets(curs)

    def display_tweets(self, curs):
        rows = curs.fetchmany(numRows = 5)

        for i, row in enumerate(rows, 1):
            print(BORDER)
            t_writer = row[1]
            t_date = convert_date(row[2])
            t_text = row[3]
            t_replyto = row[4]
            t_rt = row[5]
            writer_name = get_name(curs, t_writer)

            print("Tweet %d" % (i))

            # Indicate retweet
            if self.is_retweet(t_writer, t_rt):
                rt_name = get_name(curs, t_rt)
                print("%s Retweeted" % (rt_name))

            print("%s @%d - %s" % (writer_name, t_writer, t_date))
            print(t_text)

        print(BORDER)

    def is_retweet(self, writer, usr):
        return writer != usr


