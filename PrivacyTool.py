import tweepy

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

print("Username: " + user.screen_name + " --- Follower Count: " + str(user.followers_count))

# Retrieve stuff (Everything basically) from the user_timeline
stuff = api.user_timeline(screen_name = user.screen_name, count = 100, include_rts = True)

for tweet in stuff:
    print ("|Tweet| - " + tweet.text + "   ==  |Time| - " + tweet.created_at.strftime('%d/%m/%y -- %H:%M'))

# Sample method, used to update a status
# api.update_status('Test')
