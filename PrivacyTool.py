'''
    File Name: PrivacyTool.py
    Author: Adam Walker
    Date Created: 20/02/2017
    Date Last Modified: 09/04/2017
    Python Version: 3.6.0
'''

import tweepy
import Classes
import TweetAnalysis
import calendar
import matplotlib.pyplot as plot
import numpy as np
from collections import Counter

# Consumer keys and access tokens, used for OAuth
consumer_key = 'YUOKTebHRQH1MUv3ZlIZ3SKM3'
consumer_secret = 'FZJtpidnF24hDL6wgTAf2Tfqa8lJj8ZaVzWLbzOAdAty7cxDFe'
access_token = '4243760297-PPxt21hr8IZCPgYBegj4NqlHagPi5lOv2wgLv1Q'
access_token_secret = 'Fu6m7teENyTVs92mWUt0UKriZun1vC3Ny5o1WkwpWlM8f'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def generatePieChart(n, data, labels, explode, title, filename):
    fig = plot.figure(n)
    ax = plot.axes([0.1, 0.1, 0.8, 0.8])

    ax.pie(data, explode, labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)
    fig.savefig("Output_Images/" + filename, bbox_inches='tight')
    print("\nChart generated and saved as: " + filename)

def generateBarChart(n, data1, data2, data3, labels, legend, y_label, x_label, title, filename):
    index = np.arange(len(labels))
    bar_width = 0.3

    fig = plot.figure(n, figsize=(6, 6))
    ax = fig.add_subplot(111)

    rects1 = ax.bar(index, data1, bar_width, alpha=0.8)
    rects2 = ax.bar(index + bar_width, data2, bar_width, alpha=0.8)
    rects3 = ax.bar(index + bar_width * 2, data3, bar_width, alpha=0.8)

    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(labels)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    ax.set_title(title)
    ax.legend((rects1, rects2, rects3), legend )
    fig.savefig("Output_Images/" + filename, bbox_inches='tight')
    print("\nChart generated and saved as: " + filename)

    # plot.show()
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
    include_retweets = False
    print("/nInvalid input, defaulting to no")

account = Classes.TwitterAccount(user.screen_name, user.name, user.followers_count, user.description)

print("\n#===================================================#\n")
print("Username: " + account.username + " --- Name: " + account.realname)
print("Follower Count: " + str(account.followers))
print("Description: " + account.description)
print("\n#===================================================#\n\n")


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
        tweet = Classes.Tweet(status.text, status.created_at, status.coordinates)
        tweet.day = calendar.day_name[tweet.date.weekday()]
        if(tweet.coordinates != None):
            tweet.long = tweet.coordinates.get('coordinates', None)[0]
            tweet.lat = tweet.coordinates.get('coordinates', None)[1]
            tweet.location = TweetAnalysis.GetAddressFromCoords(tweet.lat, tweet.long)
            #print(str(tweet.coordinates.get('coordinates', 'No available data')[0]))
        account.tweets.append(tweet)

print("\nExtracted: " + str(len(account.tweets)) + " tweets.\n")

totalPos = 0
totalNeu = 0
totalNeg = 0
locationCount = 0

daysCount = [0, 0, 0, 0, 0, 0, 0]
posDays = [0, 0, 0, 0, 0, 0, 0]
negDays = [0, 0, 0, 0, 0, 0, 0]
neuDays = [0, 0, 0, 0, 0, 0, 0]

for tweet in account.tweets:
    users = TweetAnalysis.extractUsernames(tweet.text)

    for user in users:
        if (user in account.associatedUsers):
            account.associatedUsers[user] += 1
        else:
            account.associatedUsers[user] = 1

    vs = TweetAnalysis.getSentimentScores(tweet.text)
    val = TweetAnalysis.getSentimentClass(vs)

    if (val > 0):
        totalPos += 1
    elif (val == 0):
        totalNeu += 1
    else:
        totalNeg += 1
    tweet.sentiment = list(vs.values())[3]

    if(tweet.coordinates != None):
        locationCount += 1

    if(tweet.day == 'Monday'):
        if(tweet.sentiment > 0):
            posDays[0] += 1
        elif(tweet.sentiment < 0):
            negDays[0] += 1
        else:
            neuDays[0] += 1
        daysCount[0] += 1
    elif(tweet.day == 'Tuesday'):
        if(tweet.sentiment > 0):
            posDays[1] += 1
        elif(tweet.sentiment < 0):
            negDays[1] += 1
        else:
            neuDays[1] += 1
        daysCount[1] += 1
    elif(tweet.day == 'Wednesday'):
        if(tweet.sentiment > 0):
            posDays[2] += 1
        elif(tweet.sentiment < 0):
            negDays[2] += 1
        else:
            neuDays[2] += 1
        daysCount[2] += 1
    elif(tweet.day == 'Thursday'):
        if(tweet.sentiment > 0):
            posDays[3] += 1
        elif(tweet.sentiment < 0):
            negDays[3] += 1
        else:
            neuDays[3] += 1
        daysCount[3] += 1
    elif(tweet.day == 'Friday'):
        if(tweet.sentiment > 0):
            posDays[4] += 1
        elif(tweet.sentiment < 0):
            negDays[4] += 1
        else:
            neuDays[4] += 1
        daysCount[4] += 1
    elif(tweet.day == 'Saturday'):
        if(tweet.sentiment > 0):
            posDays[5] += 1
        elif(tweet.sentiment < 0):
            negDays[5] += 1
        else:
            neuDays[5] += 1
        daysCount[5] += 1
    elif(tweet.day == 'Sunday'):
        if(tweet.sentiment > 0):
            posDays[6] += 1
        elif(tweet.sentiment < 0):
            negDays[6] += 1
        else:
            neuDays[6] += 1
        daysCount[6] += 1

d = Counter(account.associatedUsers)
d.most_common()
print("Top 3 most tweeted to users by: " + str(account.realname))
for k, v in d.most_common(3):
    print ('%s: %i' % (k, v))

tweetCount = len(account.tweets)
posPercent = float("{0:.2f}".format((totalPos / tweetCount) * 100))
neuPercent = float("{0:.2f}".format((totalNeu / tweetCount) * 100))
negPercent = float("{0:.2f}".format((totalNeg / tweetCount) * 100))
locationPercent = float("{0:.2f}".format((locationCount / tweetCount) * 100))

print("\nTweet count: " + str(len(account.tweets)))
print("Total Positive: " + str(totalPos) + "  |  Percentage: " + str(posPercent))
print("Total Neutral: " + str(totalNeu) + "  |  Percentage: " + str(neuPercent))
print("Total Negative: " + str(totalNeg) + "  |  Percentage: " + str(negPercent))
print ("\nTotal location enabled tweets: " + str(locationCount) + "  |  Percentage: " + str(locationPercent))

labels = ["Positive", "Negative", "Neutral"]
data = [totalPos, totalNeg, totalNeu]
title = "Tweet sentiment percentages for: " + str(account.realname)

# Dynamically adjust the exploded element of the pie chart to be the largest section
if(posPercent > negPercent and posPercent > neuPercent):
    explode = [0.1, 0, 0]
elif(negPercent > posPercent and negPercent > neuPercent):
    explode = [0, 0.1, 0]
else:
    explode = [0, 0, 0.1]

# The number is for uniquely identifying the chart figure so it doesn't add new charts over old ones
generatePieChart(1, data, labels, explode, title, "TweetSentiments.png")

labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
title = "Tweet count by day for: " + account.realname
explode = [0, 0, 0, 0, 0, 0, 0]

generatePieChart(2, daysCount, labels, explode, title, "DayCount.png")

days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
index = np.arange(len(labels))
legend = ['Positive Tweets', 'Negative Tweets', 'Neutral Tweets']

generateBarChart(3, posDays, negDays, neuDays, days, legend, "Tweets", "Days", "Tweet sentiment by day - " + account.realname, "SentimentByDay.png")

## This function is to take various pieces of data collected and
## log them out into a text file that can be used for other things
## == Ideally this should be shortened to just logging and no analysis, and also moved to the start of the code/another file == ##
def generateLogFile():
    logfile = open("Output_Log.txt", "w")

# Print each tweet and it's timestamp into a log file, with a line break every 25 for easier readability
    count = 1
    for tweet in account.tweets:
        logfile.write("|Tweet " + str(count) + "| " + tweet.text + "   ==   |Time| - " + tweet.date.strftime("%d/%m/%y -- %H:%M  ==  |Day| " + tweet.day + " ~#~\n"))
        logfile.write("\tSentiment: " + str(tweet.sentiment) + "  ==  |Coords| " + str(tweet.coordinates) + "  ==  |Location| " + tweet.location + "\n")
        if count % 25 == 0:
            logfile.write("\n\n")
        count = count+1

    logfile.close()

generateLogFile()
print("\nProgram complete. Please see output file for details.")
