
import tweepy

from tweepy.auth import OAuthHandler


consumer_key = "K5M6c7GqkyJsSfHIEQOfd74Gp"
consumer_secret = "2xVzxHqT1pvIduyHbkbOHScZvOyzT0s1WOTqJFdZhBRAuND1Qd"
access_token = "1265579879430488065-GPcUBR56elloJ30xEvRNfgxtW5GaDK"
access_token_secret = "0ShDXpeC0Yt5oxvze8T1V9U8PdAUa7GoaMmGIDqHYzryO"

# Creating the authentication object
auth = OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

# The search term you want to find
query = "trump"
# Language code (follows ISO 639-1 standards)
language = "en"

# Calling the user_timeline function with our parameters
results = api.search(q=query, lang=language)


# foreach through all tweets pulled
#for tweet in results:
   # printing the text stored inside the tweet object
   #print(tweet.user.screen_name.encode('utf-8'),"Tweeted:",tweet.text.encode('utf-8'))



WORLD_WOE_ID = 1
US_WOE_ID = 23424977

world_trends = api.trends_place(1)


data = world_trends[0] 
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
# put all the names together with a ' ' separating them
trendsName = ' '.join(names)
print(trendsName.encode('utf-8'))


