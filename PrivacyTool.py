'''
    File Name: PrivacyTool.py
    Author: Adam Walker
    Date Created: 20/02/2017
    Date Last Modified: 02/04/2017
    Python Version: 3.6.0
'''

import tweepy
import Classes
import TweetAnalysis

# Consumer keys and access tokens, used for OAuth
consumer_key = 'YUOKTebHRQH1MUv3ZlIZ3SKM3'
consumer_secret = 'FZJtpidnF24hDL6wgTAf2Tfqa8lJj8ZaVzWLbzOAdAty7cxDFe'
access_token = '4243760297-PPxt21hr8IZCPgYBegj4NqlHagPi5lOv2wgLv1Q'
access_token_secret = 'Fu6m7teENyTVs92mWUt0UKriZun1vC3Ny5o1WkwpWlM8f'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

validUser = False

while validUser == False:
    username = input("Please enter Twitter username: ")
    try:
        user = api.get_user(username)
        validUser = True
    except:
        print("Error. Unable to authenticate username, please try again.")

# Just makes it easier to change options when the program is running
retweet_input = input("Include retweets? (Y/N): ")

if retweet_input == "Y" or retweet_input == "y":
    include_retweets = True
elif retweet_input == "N" or retweet_input == "n":
    include_retweets = False
else:
    include_retweets = True
    print("/nInvalid input, defaulting to yes")

account = Classes.TwitterAccount(user.screen_name, user.name, user.followers_count)

print("Username: " + account.username + " --- Name: " + account.realname)
print("Follower Count: " + str(account.followers) + "\n\n")

# Retrieve stuff (Everything basically) from the user_timeline
#stuff = api.user_timeline(screen_name = user.screen_name, count = 200, include_rts = True)

page_list = []
n = 0

for page in tweepy.Cursor(api.user_timeline, id = user.screen_name, count = 200, include_rts = include_retweets).pages(32):
    page_list.append(page)
    n = n+1
    print(n)

for page in page_list:
    for status in page:
        tweet = Classes.Tweet(status.text, status.created_at)
        account.tweets.append(tweet)

print("\nExtracted: " + str(len(account.tweets)) + " tweets.\n")

totalPos = 0
totalNeu = 0
totalNeg = 0

for tweet in account.tweets:
    vs = TweetAnalysis.getSentimentScores(tweet.text)
    val = TweetAnalysis.getSentimentClass(vs)

    if (val > 0):
        totalPos += 1
    elif (val == 0):
        totalNeu += 1
    else:
        totalNeg += 1

tweetCount = len(account.tweets)
posPercent = float("{0:.2f}".format((totalPos / tweetCount) * 100))
neuPercent = float("{0:.2f}".format((totalNeu / tweetCount) * 100))
negPercent = float("{0:.2f}".format((totalNeg / tweetCount) * 100))

print("Tweet count: " + str(len(account.tweets)))
print("Total Positive: " + str(totalPos) + " Percentage: " + str(posPercent))
print("Total Neutral: " + str(totalNeu) + " Percentage: " + str(neuPercent))
print("Total Negative: " + str(totalNeg) + " Percentage: " + str(negPercent))

def generateLogFile():
    logfile = open("Output_Log.txt", "w")

# Print each tweet and it's timestamp into a log file, with a line break every 25 for easier readability
    count = 1
    for tweet in account.tweets:
        logfile.write("|Tweet " + str(count) + "| " + tweet.text + "   ==   |Time| - " + tweet.date.strftime('%d/%m/%y -- %H:%M ~#~\n' ))
        # vs = TweetAnalysis.getSentimentScores(tweet.text)
        # logfile.write("\t" + str(vs) + "\n")
        if count % 25 == 0:
            logfile.write("\n\n")
        count = count+1

    logfile.close()

generateLogFile()
print("\nProgram complete. Please see output file for details.")
