'''
    File Name: Classes.py
    Author: Adam Walker
    Date Created: 12/03/2017
    Date Last Modified: 08/04/2017
    Python Version: 3.6.0
'''

class TwitterAccount(object):

    def __init__(self, username, realname, followers):
        self.username = username
        self.realname = realname
        self.followers = followers
        self.tweets = []
        self.associatedUsers = {}

class Tweet(object):

    def __init__(self, text, date, coordinates):
        self.text = text
        self.date = date
        self.coordinates = coordinates
        self.lat = 0.0
        self.long = 0.0
        self.location = "N/A"
        self.sentiment = 0 # This represents whether the tweet is positive/neutral/negative via 1/0/-1
