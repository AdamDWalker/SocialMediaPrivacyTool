'''
    File Name: PrivacyTool.py
    Author: Adam Walker
    Date Created: 20/02/2017
    Date Last Modified: 21/04/2017
    Python Version: 3.6.0
'''

import tweepy
import Classes
import TweetAnalysis
import Charts
import calendar
from collections import Counter


## This function is to take various pieces of data collected and
## log them out into a text file that can be used for other things
## == Ideally this should be shortened to just logging and no analysis, and also moved to the start of the code/another file == ##
def generateLogFile():
    Charts.create_directory("Output_Logs/")
    logfile = open("Output_Logs/Total_Output_Log.txt", "w")

# Print each tweet and it's timestamp into a log file, with a line break every 25 for easier readability
    count = 1
    for tweet in account.tweets:
        logfile.write("|Tweet " + str(count) + "| " + tweet.text + "   ==   |Time| - " + tweet.date.strftime("%d/%m/%y -- %H:%M  ==  |Day| " + tweet.day + " ~#~\n"))
        logfile.write("\tSentiment: " + str(tweet.sentiment) + "  ==  |Coords| " + str(tweet.coordinates) + "  ==  |Location| " + tweet.location + "\n")
        logfile.write("\tHashtags: " + str(tweet.hashtags) + " Keywords: " + str(tweet.keywords) + "\n")
        #logfile.write("\tEntities: " + str(tweet.entities))
        if count % 25 == 0:
            logfile.write("\n\n")
        count = count+1

    logfile.close()
##
## Outputs a specific set of tweets to a file
def outputTweets(tweets, title, filename):
    Charts.create_directory("Output_Logs/")
    tweetLog = open(filename, "w")

    tweetLog.write("\t===== " + title + " =====\n\n")
    for tweet in tweets:
        tweetLog.write("\nSentiment: " + str(tweet.sentiment) + " \t Keywords: " + str(tweet.keywords) + "\n")
        tweetLog.write("\tTweet: " + tweet.text + "\n")

    tweetLog.close()

## Outputs all locations to a file
## Formats the location enabled stuff first, then location mentions
def outputLocations(isEmpty):
    locCount = 0
    Charts.create_directory("Output_Logs/")
    locFile = open("Output_Logs/Location_Log.txt", "w")

    locFile.write("\t===== Location enabled Tweets =====\n")

    if(isEmpty):
        locFile.write("No locations found for account: " + str(account.realname))
    else:
        for tweet in account.tweets:
            if (tweet.location != "N/A"):
                locFile.write("|Coords| - " + str(tweet.coordinates) + "\n")
                locFile.write("|Location| - " + tweet.location + "\n")
                locFile.write("\t|Date| - " + tweet.day + " " + tweet.date.strftime("%d/%m/%y -- %H:%M") + "\n")

    locFile.write("\n\n\t===== Location Names in text =====\n")
    if account.places:
        locFile.write("Account description locations: " + str(account.places) + "\n\n")
    else:
        locFile.write("No locations found in account description" + "\n\n")

    for tweet in account.tweets:
        if tweet.places:
            locFile.write("\nLocations: " + str(tweet.places) + "\n")
            locFile.write("\tFrom tweet: " + tweet.text + "\n")
            locCount += 1
    if(locCount == 0):
        locFile.write("\nNo locations found in tweets")
    locFile.close()

def outputUsers(isEmpty):
    Charts.create_directory("Output_Logs/")
    userLogFile = open("Output_Logs/User_Log.txt", "w")

    if(isEmpty):
        userLogFile.write("No users found for account: " + str(account.realname))
    else:
        userLogFile.write("Users tweeted to by count from account: " + str(account.realname) + "\n\n")
        for k, v in d.most_common():
            userLogFile.write('%s: %i\n' % (k, v))
    userLogFile.close()

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

# If the username isn't real, try again
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
    print("\nInvalid input, defaulting to no")

# Get the account information and create an account object to store it all.
account = Classes.TwitterAccount(user.screen_name, user.name, user.followers_count, user.description)
account.gender = TweetAnalysis.getGender(account.realname.split(None, 1)[0])

# Console debug heading information about account details
print("\n\t#===================================================#\n")
print("Username: " + account.username + " --- Name: " + account.realname)
print("Gender: " + account.gender)
print("Follower Count: " + str(account.followers))
print("Description: " + account.description)
print("\n\t#===================================================#\n\n")

place = TweetAnalysis.findPlaces(account.description)

# CHeck the account description for any place mentions
if place.cities:
    account.places.append(place.cities)
elif place.countries:
    account.places.append(place.countries)
elif place.country_mentions:
    account.places.append(place.country_mentions)
elif place.nationalities:
    account.places.append(place.nationalities)

# If the account is protected none of this will work anyway
if (user.protected == False):

    page_list = []
    n = 0

    for page in tweepy.Cursor(api.user_timeline, id = user.screen_name, count = 200, include_rts = include_retweets).pages(32):
        page_list.append(page)
        n = n+1
        print(n)

    # For each page of tweets, grab all these different bits of data and store them as tweet objects
    for page in page_list:
        for status in page:
            tweet = Classes.Tweet(status.text, status.created_at, status.coordinates)
            if(tweet.text[0] == "R" and tweet.text[1] == "T"):
                tweet.isRT = True
            tweet.day = calendar.day_name[tweet.date.weekday()]
            if(tweet.coordinates != None):
                tweet.long = tweet.coordinates.get('coordinates', None)[0]
                tweet.lat = tweet.coordinates.get('coordinates', None)[1]
                tweet.location = TweetAnalysis.GetAddressFromCoords(tweet.lat, tweet.long)
                #print(str(tweet.coordinates.get('coordinates', 'No available data')[0]))
            account.tweets.append(tweet)

    print("\nExtracted: " + str(len(account.tweets)) + " tweets.\n")

    # For percentages of tweets and whatnot
    totalPos = 0
    totalNeu = 0
    totalNeg = 0
    locationCount = 0
    totalKeywords = []
    posKeywords = []
    negKeywords = []
    posTweets = []
    negTweets = []

    daysCount = [0, 0, 0, 0, 0, 0, 0]
    posDays = [0, 0, 0, 0, 0, 0, 0]
    negDays = [0, 0, 0, 0, 0, 0, 0]
    neuDays = [0, 0, 0, 0, 0, 0, 0]

    RTCount = 0

    # This is the main loop where the tweets undergo each different NLP technique and whatever else needs doing
    for tweet in account.tweets:

        # Get these here before anything changes the tweet text
        users = TweetAnalysis.extractUsernames(tweet.text)
        tweet.hashtags = TweetAnalysis.extractHashtags(tweet.text)


        for user in users:
            if (user in account.associatedUsers):
                account.associatedUsers[user] += 1
            else:
                account.associatedUsers[user] = 1

        # Get the sentiment polarity scores, then get what sentiment class that is (e.g. pos/neg/neu)
        vs = TweetAnalysis.getSentimentScores(tweet.text)
        val = TweetAnalysis.getSentimentClass(vs)

        # Get any places mentioned in the tweet
        place = TweetAnalysis.findPlaces(tweet.text)

        if place.cities:
            tweet.places.append(place.cities)
        elif place.countries:
            tweet.places.append(place.countries)
        elif place.nationalities:
            tweet.places.append(place.nationalities)

        if(tweet.isRT == True):
            RTCount += 1

        # Keyword extraction. Roughly follows the Information extraction 'pipeline'
        # Raw text -> tokenised (and stripped of unwanted stuff) -> tagged -> NE recognition -> relation recognition
        # Using Spacy to extract keywords, gets named entities then removes the object/subject and root of the sentence for keywords.
        textTemp = TweetAnalysis.stripPunctuation(tweet.text)
        tokens = TweetAnalysis.getTokens(textTemp)
        tagged = TweetAnalysis.getTags(tokens)
        #tweet.entities = TweetAnalysis.getEntities(tagged)
        tweet.keywords = TweetAnalysis.removeStopwords(tokens)
        tweet.keywords = [keyword for keyword in tweet.keywords if keyword not in account.associatedUsers]
        tweet.keywords = [keyword for keyword in tweet.keywords if keyword not in tweet.hashtags]
        keywords = ' '.join(word for word in tweet.keywords if len(word) > 2) # Get rid of small words, since they're mostly little meaningless things that sneak through other steps anyway
        tweet.keywords = TweetAnalysis.getKeywords(keywords)
        totalKeywords.extend(tweet.keywords)

        if (val > 0):
            totalPos += 1
            posKeywords.extend(tweet.keywords)
            posTweets.append(tweet)
        elif (val == 0):
            totalNeu += 1
        else:
            totalNeg += 1
            negKeywords.extend(tweet.keywords)
            negTweets.append(tweet)
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
    RTPercent = float("{0:.2f}".format((RTCount / tweetCount) * 100))
    posPercent = float("{0:.2f}".format((totalPos / tweetCount) * 100))
    neuPercent = float("{0:.2f}".format((totalNeu / tweetCount) * 100))
    negPercent = float("{0:.2f}".format((totalNeg / tweetCount) * 100))
    locationPercent = float("{0:.2f}".format((locationCount / tweetCount) * 100))

    print("\nTweet count: " + str(len(account.tweets)) + "  |  RTs: " + str(RTCount) + "  |  Percentage: " + str(RTPercent))
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
    Charts.generatePieChart(1, data, labels, explode, title, "TweetSentiments.png")

    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    title = "Tweet count by day for: " + account.realname
    explode = [0, 0, 0, 0, 0, 0, 0]

    Charts.generatePieChart(2, daysCount, labels, explode, title, "DayCount.png")

    days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    legend = ['Positive Tweets', 'Negative Tweets', 'Neutral Tweets']

    Charts.generateBarChart(3, posDays, negDays, neuDays, days, legend, "Tweets", "Days", "Tweet sentiment by day - " + account.realname, "SentimentByDay.png")

    generateLogFile()
    outputTweets(posTweets, "Positive tweets by keyword", "Output_Logs/Positive_Tweets_Log.txt")
    outputTweets(negTweets, "Negative tweets by keyword", "Output_Logs/Negative_Tweets_Log.txt")
    if(locationCount != 0):
        outputLocations(False)
    else:
        outputLocations(True)

    if d:
        outputUsers(False)
    else:
        outputUsers(True)

    keywordString = ' '.join(totalKeywords)
    Charts.generateWordcloud(keywordString, "Tweet keywords - " + account.realname, "TotalWordcloud.png")
    posKeywordString = ' '.join(posKeywords)
    Charts.generateWordcloud(posKeywordString, "Positive tweet keywords - " + account.realname, "PosWordcloud.png")
    negKeywordString = ' '.join(negKeywords)
    Charts.generateWordcloud(negKeywordString, "Negative tweet keywords - " + account.realname, "NegWordcloud.png")
    print("\nProgram complete. Please see output files for details.")

else:
    print("#===================================================#\n")
    print("\tError: This account is protected")
    print("\n#===================================================#\n")
