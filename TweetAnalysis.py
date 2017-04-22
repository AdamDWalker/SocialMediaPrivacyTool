'''
    File Name: TweetAnalysis.py
    Author: Adam Walker
    Date Created: 05/03/2017
    Date Last Modified: 21/04/2017
    Python Version: 3.6.0
'''

import nltk, re
import gender_guesser.detector as gender
from nltk.sentiment.vader import SentimentIntensityAnalyzer as vaderSentiment
from nltk.corpus import stopwords
from geopy.geocoders import Nominatim
from geotext import GeoText
from spacy.en import English

nlp = English()
detect = gender.Detector(case_sensitive=False)
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

def stripPunctuation(tweet):
    for char in '"#?.!/;:@([])':
        tweet = tweet.replace(char,'')
    return tweet

def removeStopwords(tokens):
    stop_words = set(stopwords.words('english'))
    stop_words.update(["'re", "'ve"])
    normalised = [word for word in tokens if word.lower() not in stop_words]
    return normalised

def getKeywords(text):
    keywords = []
    text = nlp(text)
    for sentence in text.sents:
        for word in sentence:
            if(word.dep_ == "ROOT"):
                keywords.append(str(word))
            elif(word.dep_ == "nsubj"):
                keywords.append(str(word))
            elif(word.dep_ == "dobj"):
                keywords.append(str(word))
    return keywords

## Takes the text string of a tweet and returns an array of any usernames in that tweet
def extractUsernames(tweet):
    usernames = re.findall(r'@([A-Za-z0-9_]+)', tweet)
    # if(len(twitter_username_re) != 0):
    #     print(twitter_username_re)
    return usernames

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

def findPlaces(text):
    places = GeoText(text)
    return places

def getGender(name):
    gen = detect.get_gender(name)
    return gen.title()
