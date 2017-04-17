'''
    File Name: TweetAnalysis.py
    Author: Adam Walker
    Date Created: 05/03/2017
    Date Last Modified: 16/04/2017
    Python Version: 3.6.0
'''

import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as vaderSentiment
from nltk.corpus import stopwords
from geopy.geocoders import Nominatim
## This function takes a sentence and returns a dictionary containing
## the sentiment polarity scores from the vader sentiment analyser
def getSentimentScores(sentence):
    vs = vaderSentiment()
    vsVal = vs.polarity_scores(sentence)
    return vsVal

## Takes the dictionary of polarity scores and returns an integer to represent
## whether the compound score shows an overall pos/neg/neutral sentiment
def getSentimentClass(sentScores):
    if(list(sentScores.values())[3] > 0):
        #print(str(val) + " [Positive]")
        return 1
    elif(list(sentScores.values())[3] == 0):
        #print(str(val) + " [Neutral]")
        return 0
    else:
        #print(str(val) + " [Negative]")
        return -1

def getTokens(tweet):
    tokens = nltk.word_tokenize(tweet)
    return tokens

def getTags(tokens):
    tagged = nltk.pos_tag(tokens)
    return tagged

def getEntities(tagged):
    entities = nltk.chunk.ne_chunk(tagged)
    return entities

def removeStopwords(tokens):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    normalised = [word for word in tokens if word.lower() not in stop_words]
    return normalised

## Takes the text string of a tweet and returns an array of any usernames in that tweet
def extractUsernames(tweet):
    twitter_username_re = re.findall(r'@([A-Za-z0-9_]+)', tweet)
    # if(len(twitter_username_re) != 0):
    #     print(twitter_username_re)
    return twitter_username_re

def extractHashtags(tweet):
    hashtags = re.findall(r'#([A-Za-z0-9]+)', tweet)
    # if(len(twitter_username_re) != 0):
    #     print(twitter_username_re)
    return hashtags

## Take lat and long, convert to a string for the function format and return the address from a reverse lookup
def GetAddressFromCoords(lat, long):
    coords = str(lat) + ", " + str(long)
    geolocator = Nominatim()
    location = geolocator.reverse(coords)
    return location.address

if __name__ == '__main__':
    with open("Output_Log.txt") as f:
        tweets = f.read().split('~#~')
    # you may also want to remove whitespace characters like `\n` at the end of each line
    #tweets = [x.strip('\n') for x in content]

    # tokens = nltk.word_tokenize(sentence)
    # tagged = nltk.pos_tag(tokens)
    # entities = nltk.chunk.ne_chunk(tagged)
