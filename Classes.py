

class TwitterAccount(object):

    def __init__(self, username, realname, followers):
        self.username = username
        self.realname = realname
        self.followers = followers
        self.tweets = []

class Tweet(object):

    def __init__(self, text, date):
        self.text = text
        self.date = date
