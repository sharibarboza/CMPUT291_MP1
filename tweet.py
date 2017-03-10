from utils import *
from queries import * 

def compose_tweet(session, menu_func=None, replyto=None):
    """ Generates a new tweet and inserts it into the database
    Also inserts any hashtags into hashtags and mentions tables

    :param session: Session object 
    :param user: logged in user's id
    :param replyto (optional): the user id of who the tweet is replying to
    """
    new_tweet = create_tweet(session, menu_func, replyto)
 
    confirm = validate_yn("Confirm tweet? y/n: ", session)
    if confirm in ["n", "no"]:
        print("Tweet cancelled.")
        return None if menu_func is None else menu_func() 
             
    insert_tweet(session.get_conn(), new_tweet.get_values())
    new_tweet.insert_terms()

    print("Tweet %d created - %s." % (new_tweet.tid(), new_tweet.tdate()))
    print("Hashtags mentioned: %s" % (new_tweet.get_terms()))
    press_enter(session)

def create_tweet(session, menu_func, replyto):
    """Gets info for new tweet and creates new Tweet object

    :param session: Session object
    :param user: logged in user id
    :param menu_func: function to return to if user quits
    :param replyto: id of user to replyto or None
    """
    text = validate_str("Enter tweet: ", session, menu_func=menu_func, null=False)
    if len(text) > 80:
        print("Tweet is too long. Must be 80 characters or less.")
        return create_tweet(session, menu_func, replyto)
  
    print_border(thick=False)
    writer = session.get_username()
    tid = generate_tid(session.get_conn())
    date = TODAY
    replyto = replyto
    rt_user = None
    data = [tid, writer, date, text, replyto, rt_user]
    new_tweet = Tweet(session, data)
    new_tweet.display(result="Tweet")
    print_border(thick=False)
    new_tweet.set_terms()

    if not new_tweet.valid_terms():
        return create_tweet(session, menu_func, replyto)
    
    return new_tweet

   
def generate_tid(conn):
    """Generates a new unique tweet id
    
    :param conn: session connection
    """
    curs = conn.cursor()
    select(curs, 'tweets')
    new_tid = len(curs.fetchall()) + 1
    
    while tid_exists(curs, new_tid): 
        new_tid += 1
    curs.close()

    return new_tid


def search_tweets(session):
    """Match tweets to user's keywords

    :param session: session connection
    :param user: logged in user id
    """
    search_input = validate_str("Enter keywords for tweet search: ", session, session.home, null=False)
    s_tweets = TweetSearch(session, search_input)
    s_tweets.get_search_tweets()
    return s_tweets 


class Tweet:

    def __init__(self, session, data):
        """ Represents a single tweet, helps to display tweets to console
        
        param conn: database session connection 
        param user: logged in user (not the tweet writer)
        param data: row values from tweets table corresponding to columns 
        """
        self.session = session
        self.conn = session.get_conn() 
        self.curs = session.get_curs() 
        self.user = session.get_username() 

        self.id = data[0]
        self.writer = data[1]
        self.date = data[2]
        self.text = data[3].rstrip()
        self.replyto = data[4]

        if len(data) > 5: 
            self.rt_user = data[5]
        else:
            self.rt_user = None

        if self.replyto:
            self.reply_user = get_user_from_tid(self.curs, self.replyto)
            self.reply_name = get_name(self.curs, self.reply_user)
            self.reply_text = get_text_from_tid(self.curs, self.replyto)

        self.date_str = convert_date(self.date)
        self.rep_cnt = get_rep_cnt(self.curs, self.id)
        self.ret_cnt = get_ret_cnt(self.curs, self.id)
        self.writer_name = get_name(self.curs, self.writer)
        
        self.terms = get_hashtags(self.curs, self.id)
        if self.terms is None: 
            self.terms = []

    def author(self):
        """Return the tweet writer"""
        return self.writer

    def retweeter(self):
        """Return the id of retweeter"""
        return self.rt_user

    def tdate(self):
        """Return the tweet date"""
        return self.date_str

    def tid(self):
        """Return the tweet id"""
        return self.id

    def get_text(self):
        """Get the tweet text"""
        return self.text

    def tweet_menu(self):
        """Displays options to reply or retweet a tweet after it has 
        been selected
        Returns the selected option from the tweet menu
        """
        choices = ["Reply", "Retweet", "Go back", "Do another search", "Home", "Logout"]
        print_border(thick=True)
        display_selections(choices)

        return choices

    def display(self, index=None, rt_user=None, result="Result"):
        """ Displays basic info on a tweet
        Used for first screen after login or a tweet search
      
        :param index (optional): tweet number (1-5)  
        :param user (optional): user id of the user who retweeted this tweet
        """
        if index is not None: 
            tweet_index = "%s %d" % (result, index + 1)
        else:
            tweet_index = "%s %d" % (result, self.id)

        col1_width = len(tweet_index) + 1
        col2_width = BORDER_LEN - col1_width - 3 
        date_line = "%s" % (self.date_str)
        date_user = "%d (%s) - %s" % (self.writer, self.writer_name, date_line)
        blank = " " * col1_width
       
        if self.replyto is not None:
            text_str = "@%s %s" % (self.reply_user, self.text)
        else:
            text_str = self.text
        text1, text2 = self.split_text(text_str)

        line1_1 = "{:{width}}".format(tweet_index, width=col1_width)
        line1_2 = "  {:{width}}".format(date_user, width=col2_width)
        line2_2 = "  {:{width}}".format(text1, width=col2_width)
        line3_2 = "  {:{width}}".format(text2, width=col2_width)
        line4_2 = "  {:{width}}".format(" ", width=col2_width)

        if rt_user is not None:
            user_name = get_name(self.curs, rt_user)
            retweeted = "%s Retweeted" % user_name
            line4_2 = line3_2
            line3_2 = line2_2
            line2_2 = line1_2
            line1_2 = "  {:{width}}".format(retweeted, width=col2_width)

        print_string(line1_1 + line1_2)
        print_string(blank + line2_2)
        
        if line3_2[2] != " ": 
            print_string(blank + line3_2)
        if line4_2[2] != " ":
            print_string(blank + line4_2)

    def split_text(self, text, max_width=65):
        """Splits up tweets text into 2 separate lines if too long"""
        space_index = -1
        text = text + " "
        text1 = text
        text2 = ""

        if len(text) > max_width:
            space_index = text.find(' ', max_width-5)
        
        if space_index >= max_width:
            space_index = 0

            i = max_width
            while text[i] != ' ': 
                i -= 1
            space_index = i
        
        if space_index > 0:    
            text1 = text[:space_index]
            text2 = text[space_index + 1:]

        return (text1, text2)

    def display_stats(self):
        """ Displays statistics on a tweet after a tweet has been selected"""
        print_newline() 
        print_border(thick=True)
        print_string("Tweet Statistics".upper())
        print_border(thick=True, sign='|')

        text1, text2 = self.split_text(self.text, max_width=75)
        print_string(text1)
        if len(text2) > 1: 
            print_string(text2)
        print_newline(no_border=False)

        print_string("Tweet ID: %d" % (self.id))
        print_string("Written by: %s @%d" % (self.writer_name, self.writer))
        print_string("Posted: %s" % (self.date_str))

        if (self.replyto):
            print_string("Reply to: (%s @%d)" % (self.reply_name, self.reply_user))
        else:
            print_string("Reply to: None")

        print_string("Number of replies: %s" % (self.rep_cnt))
        print_string("Number of retweets: %s" % (self.ret_cnt))
        
        choices = self.tweet_menu()
        choice = validate_num(SELECT, self.session, self.session.home, size=len(choices))
        return choices[choice-1]

    def reply(self, menu_func=None):
        """Reply to the Tweet

        :param menu_func: return point if user decides to cancel reply
        """
        compose_tweet(self.session, menu_func, replyto=self.id)

    def retweet(self, menu_func=None):
        """Allows logged in user to retweet a selected tweet"""
        if already_retweeted(self.curs, self.user, self.id):
            print_border(thick=False)
            print_string("You already retweeted this tweet.")
            print_border(thick=False)
            return None if menu_func is None else menu_func()
            
        print_border(thick=False)
        self.display(rt_user=self.user)
        print_border(thick=False)

        confirm = validate_yn("Confirm retweet? y/n: ", self.session)
        if confirm in ["n", "no"]:
            print("Retweet cancelled.")
            
        else:
            print("Retweeted - %s" % (convert_date(TODAY)))
            data_list = [self.user, self.id, TODAY]
            insert_retweet(self.conn, data_list)

            press_enter(self.session)

    def get_values(self):
        """Returns a list of tid, writer, tdate, text, and replyto"""
        return [self.id, self.writer, self.date, self.text, self.replyto]

    def match_text(self, word):
        """Return True if search keyword matches a text (but not hashtag)

        :param word: keyword string
        """
        if word not in self.terms and word in self.raw_text:
            return True
        else:
            return False

    def get_terms(self):
        """Returns the list of hashtag terms for the tweet"""
        return self.terms

    def set_terms(self):
        """Finds the hashtags in a tweet and returns the terms""" 
        hashtags = self.find_hashtags() 

        for tag in hashtags:
            term = self.extract_term(tag).lower()
            self.terms.append(term)
        
    def insert_terms(self):
        """Inserts all hashtag terms into the hashtags table"""
        for term in self.terms:
            if not hashtag_exists(self.curs, term):
                insert_hashtag(self.conn, term)      
 
            if not mention_exists(self.curs, self.id, term):
                insert_mention(self.conn, [self.id, term])
 
    def valid_terms(self):
        """Returns True if all terms do not exceed restriction length"""
        for term in self.terms:
            if len(term) > 10:
                print_string("%s is too long. Must be 10 characters or less.\n" % (term))
                self.terms = []
                return False
        return True

    def get_nohash(self):
        """Return tweet text without the hashtags"""
        text_str = self.text.lower()
        for word in self.terms:
            word = '#' + word
            text_str = text_str.replace(word, '')
        return text_str

    def extract_term(self, index):
        """Gets the hashtag term in the tweet based on the index
        
        :param index: the index of the hashtag in the tweet text
        Returns the hashtag term
        """
        space_index = self.text.find(' ', index)
        if space_index < 0:
            space_index = len(self.text) + 1

        return self.text[index+1:space_index]

    def find_hashtags(self):
        """ Returns a list of all indexes of found hashtags"""
        index_list = []
        for i, ch in enumerate(self.text):
            if ch == '#':
                index_list.append(i)
        return index_list

class TweetSearch:

    def __init__(self, session, keywords=''):
        """Can be used for getting tweets of users being 
        followed or searching for specific tweets based on keywords
         
        param session: database session connection
        param user: logged in user id
        """ 
        self.session = session
        self.conn = session.get_conn() 
        self.user = session.get_username() 
        self.tweetCurs = self.session.get_curs() 
        self.all_tweets = []
        self.tweets = []
        self.more_exist = False
        self.tweet_index = 5
        self.rows = None
        self.searched = keywords
        self.keywords = convert_keywords(keywords)
        self.logged_user = "Logged in: %d (%s)" % (self.user, self.session.get_name())

        if len(keywords) > 0:
            self.category = "TweetSearch"
        else:
            self.category = "Home"

    def get_category(self):
        return self.category

        if len(keywords) > 0:
            self.category = "TweetSearch"
        else:
            self.category = "Home"

    def get_category(self):
        return self.category

    def get_searched(self):
        width = 50
        if len(self.searched) > width:
            return self.searched[:width] + "..."
        else:
            return self.searched

    def get_search_tweets(self):
        """Find tweets matching keywords"""
        match_tweet(self.tweetCurs, self.keywords, 'tdate')
        self.add_filtered_results()
        self.more_results()

    def get_user_tweets(self):
        """Find tweets/retweets from users who are being followed"""
        follows_tweets(self.tweetCurs, self.user)
        self.add_results()
        self.more_results()

    def add_results(self):
        """Adds tweets from the query resuls into the all_tweets list"""
        for row in self.tweetCurs.fetchall():
            tweet = Tweet(self.session, row)
            self.all_tweets.append(tweet)

    def add_filtered_results(self):
        """Remove tweets from all_tweets list if the tweet does not match
        a keyword
        """
        for row in self.tweetCurs.fetchall():
            tweet = Tweet(self.session, data=row)
            valid_tweet = True
            if len(self.keywords) > 0:
                valid_tweet = self.validate_tweet(tweet)

            if valid_tweet:
                self.all_tweets.append(tweet)

    def validate_tweet(self, tweet):
        """Returns true if a keyword is not a hashtag and the tweet does not mention it

        :param tweet: Tweet object
        """
        terms = tweet.get_terms()
        for word in self.keywords:
            if is_hashtag(word) and word.replace('#', '') in terms:
               return True
            elif not is_hashtag(word) and word in tweet.get_nohash():
               return True 
        return False 

    def more_results(self):
        """Gets the next 5 tweets from users who are being followed"""
        assert(self.tweetCurs is not None), 'Unable to select more tweets'

        self.tweets = self.all_tweets[self.tweet_index - 5:self.tweet_index]
        self.more_exist = len(self.all_tweets) - self.tweet_index > 0
        self.tweet_index += 5
  
    def display_results(self):
        """Display resulting tweets 5 at a time ordered by date"""
        print_border(thick=True) 
        if self.category == "TweetSearch": 
            title = "SEARCH RESULTS FOR %s" % (self.get_searched().upper())
            print_string(title)
        else: 
            title = "HOME"
            split_title(title, self.session.get_name().upper())
        print_border(thick=True, sign='|') 

        for i, tweet in enumerate(self.tweets):
            rt_user = tweet.retweeter()
            if rt_user and tweet.author() != rt_user: 
                tweet.display(index=i, rt_user=rt_user)
            else:
                tweet.display(index=i)

            if i == len(self.tweets) - 1:
                print_border(thick=False, sign='+')
            else:
                print_border(thick=False, sign='|')

        if len(self.tweets) == 0:
            if len(self.keywords) > 0:
                print_string("Sorry, there are no tweets that match that query.")
            else:
                print_string("You have no tweets yet.")
            print_border(thick=False, sign='|')

    def select_result(self, tweet):
        """Prompt user to choose one of the displayed tweets
        
        Returns selected option from tweet menu 
        """
        option = tweet.display_stats()

        if option == "Reply":
            tweet.reply()
            self.select_result(tweet)
        elif option == "Retweet":
            tweet.retweet()         
            self.select_result(tweet)                
        elif option == "Go back":
            self.session.home(self) 
        elif option == "Do another search":
            new_search = search_tweets(self.session)
            self.session.home(new_search)
        elif option == "Home":
            self.session.home()
        elif option == "Logout":
            self.session.logout()

        self.session.home(self)
            
    def choose_result(self):
        """Returns the number of the tweet the user wants to select"""
        prompt = "Enter the result number to select: "
        choice = validate_num(prompt, self.session, size=len(self.tweets))
        if check_quit(choice):
            self.session.home(self)
        else:
            choice -= 1

        tweet = self.tweets[choice]
        self.select_result(tweet)

    def results_exist(self):
        """Return true if user has tweets to display"""
        return True if len(self.tweets) > 0 else False

    def more_results_exist(self):
        """Return true if more tweets can be displayed"""
        return self.more_exist
